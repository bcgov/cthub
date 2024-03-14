from decimal import Decimal
import pandas as pd
import traceback
from django.db import transaction

def get_field_default(model, field):
    field = model._meta.get_field(field)
    
    if callable(field.default):
        return field.default()
    return field.default

def get_nullable_fields(model):
    nullable_fields = {}

    for field in model._meta.get_fields():
        if hasattr(field, 'null') and field.null:
            nullable_fields[field.name] = True
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
        traceback.print_exc()
        raise


def transform_data(df, dataset_columns, column_mapping_enum, preparation_functions=[], validation_functions=[]):
    required_columns = [col.value for col in dataset_columns]

    df = df[[col for col in df.columns if col in required_columns]]

    missing_columns = [col for col in required_columns if col not in df.columns]
    if missing_columns:
        raise ValueError(f"Missing columns: {', '.join(missing_columns)}")
    
    for prep_func in preparation_functions:
        df = prep_func(df)

    for validate in validation_functions:
        df = validate(df)
    
    column_mapping = {col.name: col.value for col in column_mapping_enum}
    # Need to use the inverse (keys) for mapping the columns to what the database expects in order to use enums
    inverse_column_mapping = {v: k for k, v in column_mapping.items()}
    df.rename(columns=inverse_column_mapping, inplace=True)

    return df

@transaction.atomic
def load_data(df, model, field_types, replace_data, user):
    row_count = 0
    records_inserted = 0
    errors = []
    nullable_fields = get_nullable_fields(model)

    if replace_data:
        model.objects.all().delete()

    for index, row in df.iterrows():
        row_dict = row.to_dict()
        valid_row = True

        for column, value in row_dict.items():

            expected_type = field_types.get(column)
            is_nullable = column in nullable_fields

            if pd.isna(value) or value == '':
                if is_nullable:
                    row_dict[column] = None
                else:
                    row_dict[column] = get_field_default(model, column)
            elif expected_type == float and isinstance(value, int):
                row_dict[column] = float(value)
            elif expected_type == int and (isinstance(value, str) and value.strip() != '') or isinstance(value, float):
                try:
                    row_dict[column] = int(value)
                except ValueError:
                    errors.append(f"Row {index + 1}: Unable to convert value to int for '{column}'. Value was '{value}'.")
                    valid_row = False
                    break
            elif expected_type == Decimal and (isinstance(value, int) or isinstance(value, float)):
                try:
                    row_dict[column] = Decimal(value)
                except ValueError:
                    errors.append(f"Row {index + 1}: Unable to convert value to int for '{column}'. Value was '{value}'.")
                    valid_row = False
                    break
            elif not isinstance(value, expected_type) and value != '':
                errors.append(f"Row {index + 1}: Incorrect type for '{column}'. Expected {expected_type.__name__}, got {type(value).__name__}.")
                valid_row = False
                break

        if valid_row:
            try:
                row_dict['update_user'] = user
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
        "errors": errors
    }


def import_from_xls(excel_file, sheet_name, model, dataset_columns, header_row, column_mapping_enum, field_types, replace_data, user, preparation_functions=[], validation_functions=[]):
    try:
        df = extract_data(excel_file, sheet_name, header_row)
        df = transform_data(df, dataset_columns, column_mapping_enum, preparation_functions, validation_functions)
        result = load_data(df, model, field_types, replace_data, user)

        if result['errors']:
            return {"success": False, "message": f"{result['records_inserted']} records inserted from {result['row_count']} total possible rows.", "errors": result['errors'], "rows_processed": result['row_count']}
        else:
            return {"success": True, "message": f"{result['records_inserted']} records inserted from {result['row_count']} total possible rows.", "rows_processed": result['row_count']}
    except Exception as error:
        traceback.print_exc()
        error_msg = f"Unexpected error: {str(error)}"
        print(error_msg)
        return {"success": False, "errors": [str(error)], "rows_processed": 0}
