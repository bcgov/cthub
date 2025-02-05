import urllib.request
import os
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from django.http import JsonResponse, FileResponse
import pathlib
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.utils.decorators import method_decorator
from api.decorators.permission import check_upload_permission
from api.models.datasets import Datasets
from api.serializers.datasets import DatasetsSerializer
from api.services.minio import generate_presigned_url, minio_get_object, minio_remove_object
from api.services.datasheet_template_generator import generate_template
from api.services.spreadsheet_uploader import import_from_xls
import api.constants.constants as constants
from api.services.spreadsheet_uploader_prep import *
from api.services.uploaded_vins_file import create_vins_file
from api.services.file_requirements import get_file_requirements
from api.serializers.file_requirements import FileRequirementsSerializer

TEMP_CLEANED_DATASET = {}

class UploadViewset(GenericViewSet):
    permission_classes = (AllowAny,)
    http_method_names = ["post", "put", "get"]

    @action(detail=False, methods=["get"])
    def datasets_list(self, request):

        incomplete_datasets = [
            "LDV Rebates",
            "Public Charging",
            "EV Charging Rebates",
            "Hydrogen Fueling",
            "Hydrogen Fleets",
            "Data Fleets",
            "Scrap It",
        ]

        datasets = Datasets.objects.all().exclude(name__in=incomplete_datasets)
        serializer = DatasetsSerializer(datasets, many=True, read_only=True)
        serializer_data = serializer.data
        serializer_data.append({"id": -1, "name": "ICBC Vins"})
        return Response(serializer_data)

    @action(detail=False, methods=["post"])
    @method_decorator(check_upload_permission())
    def import_data(self, request):
        filename = request.data.get("filename")
        dataset_selected = request.data.get("datasetSelected")
        replace_data = request.data.get("replaceData", False)
        filepath = request.data.get("filepath")
        check_for_warnings = request.data.get("checkForWarnings")
        #boolean, if true show warnings before inserting data
        #after displaying warnings, code can be rerun with show_warnings = false
        #if warnings have been ignore

        if dataset_selected == "ICBC Vins":
            file_extension = pathlib.Path(filepath).suffix
            if file_extension == '.csv':
                try:
                    create_vins_file(filename)
                    return Response({"success": True, "message": "File successfully uploaded!"}, status=status.HTTP_200_OK)
                except Exception as error:
                    return Response({"success": False, "message": str(error)})
            else:
                return Response({"success": False, "message": "File must be a csv."}, status=status.HTTP_400_BAD_REQUEST)
        try:
            url = minio_get_object(filename)
            urllib.request.urlretrieve(url, filename)

            config = constants.DATASET_CONFIG.get(dataset_selected)
            if not config:
                return Response(
                    f"Dataset '{dataset_selected}' is not supported.",
                    status=status.HTTP_400_BAD_REQUEST,
                )
            model = config["model"]
            columns = config.get("columns")
            mapping = config.get("column_mapping")
            sheet_name = config.get(
                "sheet_name", "Sheet1"
            )  # Default to 'Sheet1' if not specified
            preparation_functions = config.get("preparation_functions", [])
            validation_functions = config.get("validation_functions", [])
            header_row = config.get("header_row", 0)

            result = import_from_xls(
                excel_file=filename,
                sheet_name=sheet_name,
                model=model,
                header_row=header_row,
                preparation_functions=preparation_functions,
                validation_functions=validation_functions,
                dataset_columns=columns,
                column_mapping_enum=mapping,
                field_types=constants.FIELD_TYPES.get(dataset_selected),
                replace_data=replace_data,
                user=request.user,
                check_for_warnings=check_for_warnings,
                temp_cleaned_dataset=TEMP_CLEANED_DATASET
            )

            if not result["success"]:
                return Response(result, status=status.HTTP_400_BAD_REQUEST)
            return Response(result, status=status.HTTP_201_CREATED)

        except Exception as e:
            return Response(
                f"An error occurred: {str(e)}", status=status.HTTP_400_BAD_REQUEST
            )

        finally:
            os.remove(filename)
            minio_remove_object(filename)

    @action(detail=False, methods=["get"])
    def download_dataset(self, request):
        dataset_name = request.GET.get("datasetSelected")
        if not dataset_name:
            return HttpResponse("Dataset name is required.", status=400)

        try:
            excel_file = generate_template(dataset_name)
            response = HttpResponse(
                excel_file.read(),
                content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            response["Content-Disposition"] = (
                f'attachment; filename="{dataset_name}.xlsx"'
            )
            return response
        except ValueError as e:
            return HttpResponse(str(e), status=400)
        
    @action(detail=False, methods=["get"])
    def file_requirements(self, request):
        dataset_name = request.query_params.get("dataset")
        file_requirements = get_file_requirements(dataset_name)
        if file_requirements is None:
            return Response({})
        serializer = FileRequirementsSerializer(file_requirements)
        return Response(serializer.data)
    
    @action(detail=False, methods=["get"])
    def download_clean_dataset(self, request):
        """Generate and return a presigned URL for downloading the cleaned dataset from MinIO."""
        try:
            dataset_key = request.GET.get("key")
            if not dataset_key:
                return JsonResponse({"success": False, "error": "Missing dataset key"}, status=400)

            presigned_url = generate_presigned_url(dataset_key)

            return JsonResponse({
                "success": True,
                "presigned_url": presigned_url,
                "filename": f"{dataset_key}.xlsx"
            })

        except Exception as e:
            return JsonResponse({"success": False, "error": str(e)}, status=500)