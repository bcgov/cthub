from decimal import Decimal, ROUND_HALF_UP
import io
import uuid
import pandas as pd
import traceback
import numpy as np
from django.db import transaction
from datetime import datetime, date
from api.services.minio import get_minio_client
from django.conf import settings

def get_field_default(model, field):
    field = model._meta.get_field(field)

    if callable(field.default):
        return field.default()
    return field.default


def get_nullable_fields(model):
    nullable_fields = []

    for field in model._meta.get_fields():
        if hasattr(field, "null") and field.null:
            nullable_fields.append(field.name)
    return nullable_fields


def trim_all_columns(df):
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def extract_data(excel_file, sheet_name, header_row):
    try:
        df = pd.read_excel(excel_file, sheet_name, header=header_row)
        df = trim_all_columns(df)
        return df
    except Exception as e:
        return None


def transform_data(
    df,
    dataset_columns,
    column_mapping_enum,
    field_types,
    model,
    preparation_functions=[],
    validation_functions=[]
):
    required_columns = [col.value for col in dataset_columns]

    df = df[[col for col in df.columns if col in required_columns]]

    errors_and_warnings = {}
    file_adjusted = False

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        errors_and_warnings['Headers'] = {}
        errors_and_warnings['Headers']['Missing Headers'] = {
            "Expected Type": "Missing one or more required columns",
            "Rows": missing_columns,
            "Severity": "Critical"
        }
        return df, errors_and_warnings, file_adjusted

    for prep_func in preparation_functions:
        df = prep_func(df)

    nullable_fields = get_nullable_fields(model)

    column_mapping = {e.value: e.name for e in column_mapping_enum}

    type_to_string = {
        int: "Integer",
        float: "Float",
        Decimal: "Decimal",
        str: "String",
        datetime.date: "Date (YYYY-MM-DD)"
    }

    df = df.replace({np.nan: None})

    for index, row in df.iterrows():
        row_dict = row.to_dict()

        for column, value in row_dict.items():
            db_field_name = column_mapping.get(column)

            if db_field_name:
                is_nullable = db_field_name in nullable_fields
                expected_type = field_types.get(db_field_name)

                if pd.isna(value) or value == "" or value is None:
                    if is_nullable:
                        row_dict[column] = None
                    else:
                        if column not in errors_and_warnings:
                            errors_and_warnings[column] = {}
                        if "Empty Value" not in errors_and_warnings[column]:
                            errors_and_warnings[column]["Empty Value"] = {
                                "Expected Type": "Cells in this column cannot be blank.",
                                "Rows": [],
                                "Severity": "Error"
                            }
                        errors_and_warnings[column]["Empty Value"]["Rows"].append(index + 2)
                else:
                    if expected_type:
                        try:
                            converted_value = value
                            if expected_type == int:
                                converted_value = int(float(value))
                            elif expected_type == float:
                                converted_value = float(value)
                            elif expected_type == Decimal:
                                converted_value = Decimal(value).quantize(
                                    Decimal("0.01"), rounding=ROUND_HALF_UP
                                )
                            elif expected_type == date:
                                if isinstance(value, datetime):
                                    converted_date = value.date()
                                else:
                                    converted_date = datetime.strptime(value, "%Y-%m-%d").date()
                                converted_value = converted_date
                            elif expected_type == str and type(value) == bool:
                                converted_value = str(value)

                            if value != converted_value:
                                file_adjusted = True
                                row_dict[column] = converted_value
                        except (ValueError, TypeError):
                            if column not in errors_and_warnings:
                                errors_and_warnings[column] = {}
                            if "Incorrect Type" not in errors_and_warnings[column]:
                                if expected_type == date:
                                    errors_and_warnings[column]["Incorrect Type"] = {
                                        "Expected Type": "Date in the format YYYY-MM-DD",
                                        "Rows": [],
                                        "Severity": "Error"
                                    }
                                elif expected_type == int:
                                    errors_and_warnings[column]["Incorrect Type"] = {
                                        "Expected Type": "Expected numeric",
                                        "Rows": [],
                                        "Severity": "Error"
                                    }
                                else:
                                    errors_and_warnings[column]["Incorrect Type"] = {
                                        "Expected Type": f"Expected {type_to_string.get(expected_type, str(expected_type))}",
                                        "Rows": [],
                                        "Severity": "Error"
                                    }
                            errors_and_warnings[column]["Incorrect Type"]["Rows"].append(index + 2)

    for x in validation_functions:
        validate = x["function"]
        columns = x["columns"]
        kwargs = x["kwargs"]
        warnings = validate(df, *columns, **kwargs)

        if warnings:
            for column, issues in warnings.items():
                if column not in errors_and_warnings:
                    errors_and_warnings[column] = {}
                for issue, details in issues.items():
                    if issue not in errors_and_warnings[column]:
                        if details.get("Severity", "Error") == 'Warning':
                            errors_and_warnings[column][issue] = {
                                "Expected Type": details.get("Expected Type", "Unknown"),
                                "Groups": details.get("Groups", []),
                                "Severity": details.get("Severity", "Error")
                            }
                        else:
                            errors_and_warnings[column][issue] = {
                                "Expected Type": details.get("Expected Type", "Unknown"),
                                "Rows": details.get("Rows", []),
                                "Severity": "Error"
                            }
                    else:
                        errors_and_warnings[column][issue]["Groups"].extend(details.get("Groups", []))

    column_mapping = {col.name: col.value for col in column_mapping_enum}
    inverse_column_mapping = {v: k for k, v in column_mapping.items()}
    df.rename(columns=inverse_column_mapping, inplace=True)

    return df, errors_and_warnings, file_adjusted


@transaction.atomic
def load_data(df, model, replace_data, user):
    records_inserted = 0

    if replace_data:
        model.objects.all().delete()
        
    for index, row in df.iterrows():
        row_dict = row.to_dict()
        row_dict["update_user"] = user

        model_instance = model(**row_dict)
        model_instance.save()
        records_inserted += 1

    return {
        "row_count": len(df),
        "records_inserted": records_inserted,
    }

TEMP_CLEANED_DATASET = {}

def import_from_xls(
    excel_file,
    sheet_name,
    model,
    dataset_columns,
    header_row,
    column_mapping_enum,
    field_types,
    replace_data,
    user,
    temp_cleaned_dataset,
    preparation_functions=[],
    validation_functions=[],
    check_for_warnings=True,
):
    errors_and_warnings = {}
    file_adjusted = False
    try:
        df = extract_data(excel_file, sheet_name, header_row)
        if df is not None:
            df, errors_and_warnings, file_adjusted = transform_data(
                df,
                dataset_columns,
                column_mapping_enum,
                field_types,
                model,
                preparation_functions,
                validation_functions,
            )
        
        else:
            errors_and_warnings['Spreadsheet'] = {}
            errors_and_warnings['Spreadsheet']['Missing Worksheet'] = {
                'Expected Type': 'The worksheet is missing or incorrectly named',
                'Rows': [sheet_name],
                'Severity': 'Critical'
            }

        cleaned_dataset_key = None
        if file_adjusted:
            cleaned_dataset_key = str(uuid.uuid4())

            inverse_column_mapping = {col.name: col.value for col in column_mapping_enum} 
            df_readable = df.rename(columns=inverse_column_mapping)

            for column in df_readable.columns:
                unique_values = set(df_readable[column].dropna().unique())
                if unique_values.issubset({True, False, "Yes", "No"}):
                    df_readable[column] = df_readable[column].map({True: "Yes", False: "No", "Yes": "Yes", "No": "No"})

            for column in df_readable.columns:
                if set(df_readable[column].dropna().unique()).issubset({"Yes", "No"}):
                    print(f"{column}: {df_readable[column].head()}")

            output = io.BytesIO()
            with pd.ExcelWriter(output, engine="openpyxl") as writer:
                df.to_excel(writer, index=False, sheet_name=sheet_name)
            output.seek(0)

            client = get_minio_client()
            bucket_name = settings.MINIO_BUCKET_NAME
            object_name = f"cleaned_datasets/{cleaned_dataset_key}.xlsx"

            try:
                client.put_object(
                    bucket_name=bucket_name,
                    object_name=object_name,
                    data=output,
                    length=output.getbuffer().nbytes,
                    content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                )
                print(f"File successfully uploaded to MinIO: {object_name}")
            except Exception as e:
                print(f"Error uploading to MinIO: {e}")

        if check_for_warnings:
            ## do the error checking

            if errors_and_warnings:
                return {
                    "success": True,
                    "message": "We encountered some potential errors in your data. Please choose whether to ignore them and continue inserting data or cancel upload and make edits to the data before reuploading",
                    "warning": True,
                    "errors_and_warnings": errors_and_warnings,
                    "file_adjusted": file_adjusted,
                    "cleaned_dataset_key": cleaned_dataset_key
                }
            else:
                print('no warnings')

        result = load_data(df, model, replace_data, user)

        total_rows = result["row_count"]
        inserted_rows = result["records_inserted"]

        return {
            "success": True,
            "message": f"All {inserted_rows} records successfully inserted out of {total_rows}.",
            "rows_processed": result["row_count"],
            "file_adjusted": file_adjusted,
            "cleaned_dataset_key": cleaned_dataset_key
            }
    
    except Exception as error:
        traceback.print_exc()
        error_msg = f"Unexpected error: {str(error)}"
        return {"success": False, "errors": [str(error)], "rows_processed": 0, "file_adjusted": file_adjusted}
