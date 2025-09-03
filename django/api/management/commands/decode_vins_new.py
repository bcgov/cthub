from django.core.management import BaseCommand, CommandError
import psycopg2
import traceback
from django.conf import settings
from api.models.uploaded_vin_record import UploadedVinRecord
from workers.external_apis.vinpower import batch_decode as vinpower_batch_decode
from workers.external_apis.vpic import batch_decode as vpic_batch_decode
from api.models.decoded_vin_record import VinpowerDecodedVinRecord, VpicDecodedVinRecord


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument("service", type=str, help="vinpower or vpic")
        parser.add_argument(
            "database",
            type=str,
            help="choose one of the databases specified in settings.DATABASES",
        )
        parser.add_argument("table", type=str)
        parser.add_argument("column", type=str)
        parser.add_argument("batch_size", type=int)

    def handle(self, *args, **options):
        service = options["service"]
        if service != "vinpower" and service != "vpic":
            raise CommandError("Invalid service!")
        conn_settings = settings.DATABASES.get(options["database"])
        if not conn_settings:
            raise CommandError("Invalid database!")

        try:
            connection = psycopg2.connect(
                dbname=conn_settings["NAME"],
                user=conn_settings["USER"],
                password=conn_settings["PASSWORD"],
                host=conn_settings["HOST"],
                port=conn_settings["PORT"],
            )
            cursor = connection.cursor(name="my_server_cursor")
            cursor.execute(f"SELECT {options['column']} FROM {options['table']}")
            while True:
                vins = []
                rows = cursor.fetchmany(size=options["batch_size"])
                if not rows:
                    break
                for row in rows:
                    uploaded_vin_obj = UploadedVinRecord(vin=row[0])
                    vins.append(uploaded_vin_obj)
                if service == "vinpower":
                    decoder = vinpower_batch_decode
                    model = VinpowerDecodedVinRecord
                elif service == "vpic":
                    decoder = vpic_batch_decode
                    model = VpicDecodedVinRecord
                decoded = decoder(vins)["successful_records"]
                records = []
                for vin, data in decoded.items():
                    records.append(model(vin=vin, data=data))
                model.objects.bulk_create(records, ignore_conflicts=True)
        except:
            traceback.print_exc()
        finally:
            cursor.close()
            connection.close()
