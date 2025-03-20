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
            cron="*/3 * * * *",
            q_options={"timeout": 165, "ack_failure": True},
        )
    except IntegrityError:
        pass


def schedule_batch_decode_vins_vpic():
    try:
        schedule(
            "workers.tasks.batch_decode_vins",
            "vpic",
            50,
            name="vpic_batch_decode_vins",
            schedule_type="C",
            cron="*/2 * * * *",
            q_options={"timeout": 105, "ack_failure": True},
        )
    except IntegrityError:
        pass


def schedule_batch_decode_vins_vinpower():
    try:
        schedule(
            "workers.tasks.batch_decode_vins",
            "vinpower",
            500,
            name="vinpower_batch_decode_vins",
            schedule_type="C",
            cron="*/2 * * * *",
            q_options={"timeout": 105, "ack_failure": True},
        )
    except IntegrityError:
        pass


def schedule_remove_cleaned_datasets():
    try:
        schedule(
            "workers.tasks.remove_cleaned_datasets",
            name="remove_cleaned_datasets",
            schedule_type="C",
            cron="0 6 * * *",   # 6:00 AM UTC = 10:00 PM PST = 11:00 PM PDT
            q_options={"timeout": 105, "ack_failure": True},
        )
    except IntegrityError:
        pass
