from decimal import Decimal, ROUND_HALF_UP
from rest_framework.response import Response
from rest_framework import status
import pandas as pd
import traceback
from django.db import transaction
from api.services.spreadsheet_uploader_prep import location_checker

def get_field_default(model, field):
    field = model._meta.get_field(field)

    if callable(field.default):
        return field.default()
    return field.default


def get_nullable_fields(model):
    nullable_fields = {}

    for field in model._meta.get_fields():
        if hasattr(field, "null") and field.null:
            nullable_fields[field.name] = True
    return nullable_fields


def trim_all_columns(df):
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def extract_data(excel_file, sheet_name, header_row):
    try:
        df = pd.read_excel(excel_file, sheet_name, header=header_row)
        df = df.fillna('TEMP_NULL')
        df = trim_all_columns(df)
        return df
    except Exception as e:
        traceback.print_exc()
        raise


def transform_data(
    df,
    dataset_columns,
    column_mapping_enum,
    preparation_functions=[],
    validation_functions=[],
):
    required_columns = [col.value for col in dataset_columns]

    df = df[[col for col in df.columns if col in required_columns]]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")

    for prep_func in preparation_functions:
        df = prep_func(df)

    validation_errors = {}
    for x in validation_functions:
        validate = x["function"]
        columns = x["columns"]
        kwargs = x["kwargs"]
        key = x["error_type"]
        key, errors = validate(df, columns, kwargs)
        if errors:
            validation_errors[key] = errors

    column_mapping = {col.name: col.value for col in column_mapping_enum}
    # Need to use the inverse (keys) for mapping the columns to what the database expects in order to use enums
    inverse_column_mapping = {v: k for k, v in column_mapping.items()}
    df.rename(columns=inverse_column_mapping, inplace=True)

    return df, validation_errors


@transaction.atomic
def load_data(df, model, field_types, replace_data, user, validation_errors):
    row_count = 0
    records_inserted = 0
    errors = []
    nullable_fields = get_nullable_fields(model)

    # validation_error_rows = get_validation_error_rows(errors) This may be used going forward for validation errors that cannot be overwritten.

    if replace_data:
        model.objects.all().delete()

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        valid_row = True

        for column, value in row_dict.items():
            expected_type = field_types.get(column)
            is_nullable = column in nullable_fields

            if expected_type in [int, float, Decimal] and value != 'TEMP_NULL':
                value = str(value).replace(',', '').strip()
                try:
                    if expected_type == int:
                        row_dict[column] = int(float(value))
                    elif expected_type == Decimal:
                        row_dict[column] = Decimal(value).quantize(Decimal("0.01"), rounding=ROUND_HALF_UP)
                    else:
                        row_dict[column] = float(value)
                except ValueError:
                    errors.append(
                        f"Row {index + 1}: Unable to convert value to {expected_type.__name__} for '{column}'. Value was '{value}'."
                    )
                    valid_row = False
                    continue

            if pd.isna(value) or value == "" or value == 'TEMP_NULL':
                if is_nullable:
                    row_dict[column] = None
                else:
                    row_dict[column] = get_field_default(model, column)

            elif not isinstance(row_dict[column], expected_type) and value != "":
                errors.append(
                    f"Row {index + 1}: Incorrect type for '{column}'. Expected {expected_type.__name__}, got {type(row_dict[column]).__name__}."
                )
                valid_row = False
                continue

            # if index + 1 in validation_error_rows:
            #     valid_row = False
            #     continue

        if valid_row:
            try:
                row_dict["update_user"] = user
                model_instance = model(**row_dict)
                model_instance.full_clean()
                model_instance.save()
                records_inserted += 1
            except Exception as e:
                errors.append(f"Row {index + 1}: {e}")

        row_count += 1

    return {
        "row_count": row_count,
        "records_inserted": records_inserted,
        "errors": sorted(errors, key=lambda x: int(x.split()[1][:-1])),
    }


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
    preparation_functions=[],
    validation_functions=[],
    check_for_warnings=False,
):
    try:
        df = extract_data(excel_file, sheet_name, header_row)
        df, validation_errors = transform_data(
            df,
            dataset_columns,
            column_mapping_enum,
            preparation_functions,
            validation_functions,
        )

        if check_for_warnings:
            ## do the error checking

            locations, names_from_spreadsheet = location_checker(df)
            locations_set = set(locations)
            names_without_match = [item for item in names_from_spreadsheet if item not in locations_set]

            if validation_errors:
                return {
                    "success": True,
                    "message": "We encountered some potential errors in your data. Please choose whether to ignore them and continue inserting data or cancel upload and make edits to the data before reuploading",
                    "warning": True,
                    "warnings": validation_errors,
                }
            else:
                print('no warnings')

        result = load_data(df, model, field_types, replace_data, user, validation_errors)

        total_rows = result["row_count"]
        inserted_rows = result["records_inserted"]

        if result["errors"] and result["records_inserted"] > 0:
            return {
                "success": True,
                "message": f"{inserted_rows} out of {total_rows} rows successfully inserted with some errors encountered.",
                "errors": result["errors"],
                "rows_processed": result["row_count"],
            }
        elif len(result["errors"]) > 0:
            return {
                "success": False,
                "message": "Errors encountered with no successful insertions.",
                "errors": result["errors"],
                "rows_processed": result["row_count"],
            }
        else:
            return {
                "success": True,
                "message": f"All {inserted_rows} records successfully inserted out of {total_rows}.",
                "rows_processed": result["row_count"],
            }
    except Exception as error:
        traceback.print_exc()
        error_msg = f"Unexpected error: {str(error)}"
        return {"success": False, "errors": [str(error)], "rows_processed": 0}
