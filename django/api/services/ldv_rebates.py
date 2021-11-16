import pandas as pd
from api.models.ldv_rebates import LdvRebates

def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)

def import_from_xls(excel_file):
    df = pd.read_excel(excel_file, 'Raw Data')
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

    for _, row in df.iterrows():
        try:
            LdvRebates.objects.create(
                casl_consent=row["CASL Consent"],
                date_approved=row["DATE APPROVED"],
                submission_id=row["Submission ID"],
                submission_date=row["Submission Date"],
                company_name=row["Company Name"],
                company_city=row["City"],
                applicant_name=row["Applicant Name"],
                applicant_address_1=row["Applicant Address 1"],
                applicant_address_2=row["Applicant Address 2"],
                applicant_city=row["Applicant City"],
                applicant_postal_code=row["Applicant Postal Code"],
                applicant_phone=row["Applicant Phone"],
                applicant_email=row["Applicant Email"],
                applicant_use=row["Applicant Use"],
                applicant_type=row["Applicant Type"],
                business_name=row["Business Name"],
                business_number=row["Business Number"],
                drivers_license=row["Drivers License"],
                province=row["Province"],
                msrp=row["MSRP"],
                other_incentives=row["Other Incentives"],
                document_type=row["Document Type"],
                vehicle=row["Vehicle"],
                incentive_amount=row["Incentive Amount"],
                vin=row["VIN#"],
                delivered=row["Delivered"],
                consent_to_contact=row["Consent to Contact"]
            )
        except:
            print(row)
    return True
