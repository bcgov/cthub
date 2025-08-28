from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Iterable, List, Dict, Any, Optional

from django.core.management.base import BaseCommand, CommandError
from django.db import connections
from django.utils import timezone
from django.conf import settings

from workers.external_apis.vinpower import batch_decode

from psycopg2 import sql
from psycopg2.extras import execute_values, Json
import psycopg2

ICBC_SCHEMA = None
ICBC_TABLE = "icbc"
ICBC_VIN_COL = "vin"

DECODED_SCHEMA = None
DECODED_TABLE = "vinpower_decoded_vin_record"
DECODED_VIN_COL = "vin"
DECODED_DATA_COL = "data"
OPTIONAL_CREATE_USER_COL = "create_user"
OPTIONAL_UPDATE_USER_COL = "update_user"


@dataclass
class _VinRow:
    vin: str

def _id(name: str) -> sql.Identifier:
    return sql.Identifier(name)

def _qname(table: str, schema: Optional[str]) -> sql.SQL:
    return sql.SQL(".").join([_id(schema), _id(table)]) if schema else _id(table)

def _open_write_conn():
    db = settings.DATABASES["default"]
    kwargs = dict(
        dbname=db.get("NAME"),
        user=db.get("USER"),
        password=db.get("PASSWORD"),
        host=db.get("HOST") or None,
        port=db.get("PORT") or None,
    )
    options = db.get("OPTIONS", {}) or {}
    if "sslmode" in options:
        kwargs["sslmode"] = options["sslmode"]
    conn = psycopg2.connect(**kwargs)
    conn.autocommit = True
    return conn

def _dest_has_cols(django_conn, schema: Optional[str], table: str, cols: Iterable[str]) -> Dict[str, bool]:
    present = {c: False for c in cols}
    with django_conn.cursor() as cur:
        if schema:
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_schema=%s AND table_name=%s
                """,
                [schema, table],
            )
        else:
            cur.execute(
                """
                SELECT column_name
                FROM information_schema.columns
                WHERE table_name=%s
                """,
                [table],
            )
        for (col,) in cur.fetchall():
            if col in present:
                present[col] = True
    return present

class Command(BaseCommand):
    help = (
        "Stream VINs from icbc not yet in vinpower_decoded_vin_record, decode in batches, "
        "and insert results using raw SQL (no Django models)."
    )

    def add_arguments(self, parser):
        parser.add_argument("--batch-size", type=int, default=2000, help="VINs per decode request.")
        parser.add_argument("--itersize", type=int, default=100000, help="Rows fetched per round-trip.")
        parser.add_argument("--limit", type=int, default=None, help="Optional cap on VINs to attempt.")
        parser.add_argument("--dry-run", action="store_true", help="Decode but skip inserts.")
        parser.add_argument("--sleep", type=float, default=0.0, help="Seconds to sleep between API calls.")
        parser.add_argument("--user", default="vin_decode_command",
                            help="Value for create_user/update_user if those columns exist.")

    def handle(self, *args, **opts):
        batch_size: int = opts["batch_size"]
        itersize: int = opts["itersize"]
        limit: Optional[int] = opts["limit"]
        dry_run: bool = opts["dry_run"]
        throttle_sleep: float = opts["sleep"]
        user_val: str = opts["user"]

        django_conn = connections["default"]
        if django_conn.vendor != "postgresql":
            raise CommandError("This command requires PostgreSQL.")

        write_conn = _open_write_conn()

        col_flags = _dest_has_cols(
            django_conn, DECODED_SCHEMA, DECODED_TABLE,
            [DECODED_VIN_COL, DECODED_DATA_COL, OPTIONAL_CREATE_USER_COL, OPTIONAL_UPDATE_USER_COL]
        )
        if not (col_flags.get(DECODED_VIN_COL) and col_flags.get(DECODED_DATA_COL)):
            raise CommandError(
                f"Destination table must have '{DECODED_VIN_COL}' and '{DECODED_DATA_COL}'."
            )
        has_create_user = col_flags.get(OPTIONAL_CREATE_USER_COL, False)
        has_update_user = col_flags.get(OPTIONAL_UPDATE_USER_COL, False)

        select_sql = sql.SQL("""
            SELECT DISTINCT i.{i_vin}
            FROM {i_tbl} AS i
            LEFT JOIN {d_tbl} AS d
              ON d.{d_vin} = i.{i_vin}
            WHERE d.{d_vin} IS NULL
              AND i.{i_vin} IS NOT NULL
              AND length(i.{i_vin}) = 17
        """).format(
            i_vin=_id(ICBC_VIN_COL),
            d_vin=_id(DECODED_VIN_COL),
            i_tbl=_qname(ICBC_TABLE, ICBC_SCHEMA),
            d_tbl=_qname(DECODED_TABLE, DECODED_SCHEMA),
        )
        if limit:
            select_sql = select_sql + sql.SQL(" LIMIT %s")

        total_seen = total_success = total_failed = batches = 0
        started_at = timezone.now()

        self.stdout.write(
            self.style.NOTICE(
                f"Streaming VINs from {ICBC_TABLE} -> {DECODED_TABLE} "
                f"(batch_size={batch_size}, itersize={itersize}, limit={limit or '∞'})"
            )
        )

        cursor_name = f"stream_icbc_vins_{int(time.time())}"

        with django_conn.cursor(name=cursor_name) as cur:
            cur.itersize = itersize
            if limit:
                cur.execute(select_sql, [limit])
            else:
                cur.execute(select_sql)

            buffer: List[_VinRow] = []

            def insert_successes(successes: Dict[str, Dict[str, Any]]) -> int:
                if not successes:
                    return 0

                columns = [DECODED_VIN_COL, DECODED_DATA_COL]
                template_fields = ["%s", "%s"]
                rows = [(vin, Json(payload)) for vin, payload in successes.items()]

                if has_create_user:
                    columns.append(OPTIONAL_CREATE_USER_COL)
                    template_fields.append("%s")
                    rows = [(*r, user_val) for r in rows]
                if has_update_user:
                    columns.append(OPTIONAL_UPDATE_USER_COL)
                    template_fields.append("%s")
                    rows = [(*r, user_val) for r in rows]

                insert_sql = sql.SQL("""
                    INSERT INTO {d_tbl} ({cols})
                    VALUES %s
                    ON CONFLICT ({d_vin}) DO NOTHING
                """).format(
                    d_tbl=_qname(DECODED_TABLE, DECODED_SCHEMA),
                    cols=sql.SQL(", ").join(_id(c) for c in columns),
                    d_vin=_id(DECODED_VIN_COL),
                )

                with write_conn.cursor() as wcur:
                    execute_values(
                        wcur,
                        insert_sql.as_string(wcur),
                        rows,
                        template="(" + ", ".join(template_fields) + ")",
                        page_size=1000,
                    )
                return len(rows)

            def process_buffer(records: List[_VinRow]):
                nonlocal total_success, total_failed, batches
                if not records:
                    return

                try:
                    result = batch_decode(records)
                except Exception as e:
                    self.stderr.write(self.style.ERROR(f"Decoder error on batch of {len(records)}: {e}"))
                    total_failed += len(records)
                    return

                successes: Dict[str, Dict[str, Any]] = result.get("successful_records", {}) or {}
                failed_vins: Iterable[str] = result.get("failed_vins", set()) or set()

                written = 0
                if not dry_run and successes:
                    written = insert_successes(successes)

                batch_success = written if not dry_run else len(successes)
                batch_failed = len(list(failed_vins))
                total_success += batch_success
                total_failed += batch_failed
                batches += 1

                self.stdout.write(
                    f"Batch {batches:>6}: decoded={batch_success:>5}, failed={batch_failed:>5}, "
                    f"cumulative decoded={total_success:>8}, failed={total_failed:>8}"
                )

                if throttle_sleep > 0:
                    time.sleep(throttle_sleep)

            for row in cur:
                vin = row[0]
                total_seen += 1
                buffer.append(_VinRow(vin=vin))
                if len(buffer) >= batch_size:
                    process_buffer(buffer)
                    buffer.clear()

            if buffer:
                process_buffer(buffer)
                buffer.clear()

        try:
            write_conn.close()
        except Exception:
            pass

        elapsed = (timezone.now() - started_at).total_seconds()
        self.stdout.write(
            self.style.SUCCESS(
                f"Done. Streamed={total_seen}, decoded={total_success}, failed={total_failed}, "
                f"batches={batches}, elapsed={elapsed:.1f}s, dry_run={dry_run}"
            )
        )
