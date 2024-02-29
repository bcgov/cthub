import pandas as pd
import traceback

def trim_all_columns(df):
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

def import_from_xls(excel_file, dataset_name, sheet_name, model,  dataset_columns, column_mapping, field_types, preparation_functions=[], validation_functions=[]):
    row_count = 0
    records_inserted = 0
    errors = []
    try:
        try:
            df = pd.read_excel(excel_file, sheet_name)
        except Exception as e:
            traceback.print_exc()
            raise
        df = trim_all_columns(df)

        for prep_func in preparation_functions:
            df = prep_func(df)

        for validate in validation_functions:
            df = validate(df)

        required_columns = dataset_columns[dataset_name]

        df = df[[col for col in df.columns if col in required_columns]]

        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            return {"success": False, "message": f"Missing columns: {', '.join(missing_columns)}"}
        
        df.rename(columns=column_mapping[dataset_name], inplace=True)

        for index, row in df.iterrows():
            row_dict = row.to_dict()
            row_dict = {k: v for k, v in row_dict.items() if k in column_mapping.values()}
            
            skip_row = False
            for column, value in row_dict.items():
                expected_type = field_types[column]
                if not isinstance(value, expected_type) and pd.notnull(value):
                    errors.append(f"Row {index + 1}: Incorrect type for '{column}'. Expected {expected_type.__name__}, got {type(value).__name__}")
                    skip_row = True
                    break
            
            if skip_row:
                continue
            
            try:
                model.objects.create(**row_dict)
                records_inserted += 1
            except Exception as e:
                errors.append(f"Row {index + 1}: {str(e)}")
            row_count += 1
            
        final_record_count = model.objects.count()
        records_inserted_msg = f"{records_inserted} records inserted from spreadsheet from {row_count} total possible rows. This database table currently contains {final_record_count} records."
        print(records_inserted_msg)

        if errors:
            return {"success": False, "message": records_inserted_msg, "errors": errors, "rows_processed": row_count}
        return {"success": True, "message": records_inserted_msg, "rows_processed": row_count}
    except Exception as error:
        traceback.print_exc()
        error_msg = f"Unexpected error: {str(e)}"
        print(error_msg)
        return {"success": False, "errors": [str(error)], "rows_processed": row_count}