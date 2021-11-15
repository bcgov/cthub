import pandas as pd
from './models/ldv_rebates' import ldv_rebates

excel_file = '/Users/emhillie/Documents/CTHUB documents/3rd Q 2021 Summary Final for Agile team.xlsx'
df = pd.read_excel(excel_file, 'Raw Data')
def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)
df.drop(df.columns.difference([
"CASL Consent",
"DATE APPROVED",
"Submission ID",
"Submission Date",
"Company Name",
"City",
"Applicant Name",
"Applicant Address 1",
"Applicant Address 2",
"Applicant City",
"Applicant Postal Code",
"Applicant Phone",
"Applicant Email",
"Applicant Use",
"Applicant Type",
"Business Name",
"Business Number",
"Drivers License",
"Province",
"MSRP",
"Other Incentives",
"Document Type",
"Vehicle",
"Incentive Amount",
"VIN#",
"Delivered",
"Consent to Contact",
]), 1, inplace=True) 
df = trim_all_columns(df)
df = df.applymap(lambda s: s.upper() if type(s) == str else s)
df['CASL Consent'].replace(
    to_replace=['YES', 'Y'],
    value=True,
    inplace=True
)
df['CASL Consent'].replace(
    to_replace=['NO', 'N'],
    value=False,
    inplace=True
)
df['Delivered'].replace(
    to_replace=['YES', 'Y'],
    value=True,
    inplace=True
)
df['Delivered'].replace(
    to_replace=['NO', 'N', 'OEM', 'INCENTIVE_FUNDS_AVAILABLE'],
    value=False,
    inplace=True
)

df['Consent to Contact'].replace(
    to_replace=['YES', 'Y'],
    value=True,
    inplace=True
)
df['Consent to Contact'].replace(
    to_replace=['NO', 'N'],
    value=False,
    inplace=True
)
df.fillna('')

try:
            # iterate through df and check if vehicle exists, if it doesn't,
            # add it!
            for _, row in df.iterrows():