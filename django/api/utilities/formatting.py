import pandas as pd
import numpy as np

def format_case(s, case = 'skip'):
    if len(s.dropna()) != 0:
        output = (
            s[s.notna()] # I am applying this function to non NaN values only. If you do not, they get converted from NaN to nan and are more annoying to work with.
            .astype(str) # Convert to string
            .str.strip() # Strip white spaces (this dataset suffers from extra tabs, lines, etc.)
            )
        
        if case == 'title':
            return output.str.title()
        elif case == 'upper':
            return output.str.upper()
        elif case == 'lower':
            return output.str.lower()
        elif case == 'postal_code':
            return output.str.upper().str.replace(' ', '', regex=False)
        elif case == 'id':
            output = output.str.lower()
            
            valid_mask = output.str.fullmatch(r'(?:[a-z0-9]+|\d+\.0+)')
            
            if (~valid_mask).any():
                ambiguous_values = output.loc[~valid_mask].tolist()
            
                raise ValueError(
                f'Ambiguous value: {ambiguous_values}'
                )
            
            return (
                output
                .str.replace(r'\.0+$', '', regex=True)
                .str.replace(r'^0+(?=\d)', '', regex=True)
                )
        elif case == 'skip':
            return output
        else:
            raise ValueError(f"Incorrect case option: {case}")


def format_numbers(s):

    if s.empty:
        raise ValueError('Series is empty')

    output = s.replace({',': pd.NA, '': pd.NA})
    output = output[output.notna()]

    if output.empty:
        return pd.Series(index=output.index, dtype='Int64')

    string_mask = output.apply(lambda x: isinstance(x, str))

    if len(output[string_mask]) > 0:
        normalized_string = (output.loc[string_mask]
        .str.strip()
        .str.replace(' ', '', regex=False)
        )

        valid_formats = [
        r"\d+", # E.g. 123
        r"\d+\.\d+", # E.g. 5.5
        r"\d{1,3}(?:,\d{3})+(?:\.\d+)?", # E.g. 200,000 or 5,000.10
        ]
        
        valid_pattern = rf"(?:{'|'.join(valid_formats)})"
        
        invalid_mask = ~normalized_string.str.fullmatch(valid_pattern)

        if len(normalized_string[invalid_mask]) > 0:
            invalid_values = normalized_string.loc[invalid_mask].tolist()
            raise ValueError(
            f"Invalid or ambiguous number format: {invalid_values}"
            )

        normalized_string = (
            normalized_string
            .str.replace(',', '') 
        )

        string_decimal_mask = normalized_string.str.contains(r'\.')
         
        if string_decimal_mask.sum() > 0:
            normalized_string.loc[string_decimal_mask] = (
            normalized_string.loc[string_decimal_mask]
            .astype(float)
            .round(0)
            .map(int)
            )
        
        output.loc[string_mask] = normalized_string.map(int)

    float_mask = output.map(lambda x: isinstance(x, (float, np.floating)))
    output.loc[float_mask] = output.loc[float_mask].astype(float).round(0).map(int)



    return output.astype('Int64')


def preprocess_raw_file(file_path, delimiter, file_dtype_dict=None, nrows='all', dropped_columns=None, dtype_numeric_list=None, dtype_date_list=None, text_modif_dict=None):

    """Preprocesses ICBC files.

    This function makes sure the ICBC files are formatted in the same way.

    Parameters
    ----------
    file_path : Path
    delimiter : character
        Current delimiter is '|' but it could change.
    file_dtype_dict : dictionary
    nrows : integer
        The number of rows to be read. Used for debugging only.
    dropped_columns: list
        A list of columns that are dropped from the file.
    dtype_numeric_list: list
        A list of numeric columns names
    dtype_date_list: list
        A list of date column names
    text_modif_dict: dictionary 
        A dictionary with keys ('upper', 'lower', 'title) and
        a list of column names for each key   

    Returns
    -------
    A dataframe

    Examples
    --------
    >>> preprocess_raw_file(
    df_date_dict[split_date_list[0][0]]['path'], 
    df_date_dict[split_date_list[0][0]]['delimiter'],
    dropped_columns=dropped_columns, 
    file_dtype_dict=file_dtype_dict, 
    dtype_numeric_list=dtype_numbers,
    dtype_date_list=dtype_dates,
    text_modif_dict=text_modif_dict)
    """

    if nrows == 'all':
        df = pd.read_csv(
        file_path, 
        delimiter=delimiter,
        na_values=['NIL', 'Unknown', 'unknown', 'UNKNOWN'], dtype=file_dtype_dict)

    else:
        df = pd.read_csv(
            file_path, 
            delimiter=delimiter,
            nrows=nrows, na_values=['NIL', 'Unknown', 'unknown', 'UNKNOWN'], dtype=file_dtype_dict)

        
    df.columns = df.columns.str.lower()
    df.drop(columns=dropped_columns, inplace=True)
    
    numeric_cols = list(set(dtype_numeric_list).intersection(set(df.columns)))

    for col in numeric_cols:
        df[col] = format_numbers(df[col])

    date_cols = list(set(dtype_date_list).intersection(set(df.columns)))
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], yearfirst=True, utc=True).dt.date

    for key in text_modif_dict:
        col_subset = list(set(text_modif_dict[key]).intersection(df.columns))
        if len(col_subset) != 0:
            for col in col_subset:
                df[col] = format_case(df[col], case=key)

    return df