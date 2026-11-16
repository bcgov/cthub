from django.db import migrations

FORWARD = r"""
CREATE TABLE public.vinpower_reporting_attribute (
    ordinal bigint GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    json_key text UNIQUE NOT NULL,
    column_name text UNIQUE NOT NULL
);

CREATE VIEW public.vinpower_decoded_vin_report AS
SELECT id, vin FROM public.vinpower_decoded_vin_record;

CREATE FUNCTION public.extend_vinpower_report(keys text[]) RETURNS void
LANGUAGE plpgsql AS $function$
DECLARE
    attribute text;
    alias_name text;
    projection text;
BEGIN
    IF NOT EXISTS (
        SELECT 1 FROM unnest(keys) AS k(key)
        WHERE NOT EXISTS (
            SELECT 1 FROM public.vinpower_reporting_attribute a WHERE a.json_key = k.key
        )
    ) THEN
        RETURN;
    END IF;

    -- Serialize schema changes; ordinary batches with known keys take no DDL lock.
    PERFORM pg_advisory_xact_lock(764192056);
    FOR attribute IN
        SELECT DISTINCT k.key FROM unnest(keys) AS k(key)
        WHERE NOT EXISTS (
            SELECT 1 FROM public.vinpower_reporting_attribute a WHERE a.json_key = k.key
        ) ORDER BY k.key
    LOOP
        -- Reserve the attribute_ prefix for deterministic escaped names. Keep
        -- ordinary Vinpower names readable and safe for case-insensitive BI tools.
        IF attribute ~ '^[a-z][a-z0-9_]*$'
           AND octet_length(attribute) <= 63
           AND attribute NOT IN ('id', 'vin')
           AND attribute NOT LIKE 'attribute!_%' ESCAPE '!' THEN
            alias_name := attribute;
        ELSE
            alias_name := 'attribute_' || md5(attribute);
        END IF;
        INSERT INTO public.vinpower_reporting_attribute (json_key, column_name)
        VALUES (attribute, alias_name);
    END LOOP;

    SELECT string_agg(format(', data ->> %L AS %I', json_key, column_name), '' ORDER BY ordinal)
    INTO projection FROM public.vinpower_reporting_attribute;
    -- Existing column names, types and order stay fixed so dependent reports survive.
    EXECUTE 'CREATE OR REPLACE VIEW public.vinpower_decoded_vin_report AS '
        || 'SELECT id, vin' || coalesce(projection, '')
        || ' FROM public.vinpower_decoded_vin_record';
END
$function$;

-- Discover historical keys once. Subsequent writes inspect only their own batch.
SELECT public.extend_vinpower_report(array(
    SELECT DISTINCT k.key
    FROM public.vinpower_decoded_vin_record r
    CROSS JOIN LATERAL jsonb_object_keys(
        CASE WHEN jsonb_typeof(r.data) = 'object' THEN r.data ELSE '{}'::jsonb END
    ) AS k(key)
));

CREATE FUNCTION public.discover_vinpower_report_attributes() RETURNS trigger
LANGUAGE plpgsql AS $function$
BEGIN
    PERFORM public.extend_vinpower_report(array(
        SELECT DISTINCT k.key FROM new_rows r
        CROSS JOIN LATERAL jsonb_object_keys(
            CASE WHEN jsonb_typeof(r.data) = 'object' THEN r.data ELSE '{}'::jsonb END
        ) AS k(key)
    ));
    RETURN NULL;
END
$function$;

CREATE TRIGGER vinpower_report_insert AFTER INSERT
ON public.vinpower_decoded_vin_record
REFERENCING NEW TABLE AS new_rows FOR EACH STATEMENT
EXECUTE FUNCTION public.discover_vinpower_report_attributes();

CREATE TRIGGER vinpower_report_update AFTER UPDATE
ON public.vinpower_decoded_vin_record
REFERENCING NEW TABLE AS new_rows FOR EACH STATEMENT
EXECUTE FUNCTION public.discover_vinpower_report_attributes();
"""

REVERSE = """
DROP TRIGGER vinpower_report_update ON public.vinpower_decoded_vin_record;
DROP TRIGGER vinpower_report_insert ON public.vinpower_decoded_vin_record;
DROP FUNCTION public.discover_vinpower_report_attributes();
DROP FUNCTION public.extend_vinpower_report(text[]);
DROP VIEW public.vinpower_decoded_vin_report;
DROP TABLE public.vinpower_reporting_attribute;
"""


class Migration(migrations.Migration):
    dependencies = [
        ("api", "0055_remove_icbcrecord_icbc_vin_efd0d6_idx_and_more"),
    ]

    operations = [migrations.RunSQL(FORWARD, REVERSE)]
