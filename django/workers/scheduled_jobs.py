from django_q.tasks import schedule
from django.db import IntegrityError


def schedule_create_minio_bucket():
    try:
        schedule(
            "workers.tasks.create_minio_bucket",
            name="create_minio_bucket",
            schedule_type="O",
            repeats=1,
        )
    except IntegrityError:
        pass


def schedule_read_uploaded_vins_file():
    try:
        schedule(
            "workers.tasks.read_uploaded_vins_file",
            name="read_uploaded_vins_file",
            schedule_type="C",
            cron="*/15 * * * *",
            q_options={"timeout": 660, "ack_failure": True},
        )
    except IntegrityError:
        pass


def schedule_batch_decode_vins():
    try:
        schedule(
            "workers.tasks.batch_decode_vins",
            "vpic",
            50,
            name="batch_decode_vins",
            schedule_type="C",
            cron="* * * * *",
            q_options={"timeout": 60, "ack_failure": True},
        )
    except IntegrityError:
        pass
