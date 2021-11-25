import pandas as pd
from api.models.speciality_use_vehicle_incentives import SpecialityUseVehicleIncentives


def trim_all_columns(df):
    """
    Trim whitespace from ends of each value across all series in dataframe
    """
    trim_strings = lambda x: x.strip() if isinstance(x, str) else x
    return df.applymap(trim_strings)


def applicant_type(row):
    if isinstance((row["Fleet"]), str):
        return 'Fleet'
    elif isinstance((row["Individual"]), str):
        return 'Individual'
    else:
        return ''


def import_from_xls(excel_file):
    df = pd.read_excel(excel_file, 'Sheet1')
    df.drop(df.columns.difference([
        "Approvals",
        "Date",
        "Applicant Name",
        "Max Incentive Amount Requested",
        "Category",
        "Fleet",
        "Individual",
        "Incentive Paid",
        "Total Purchase Price (pre-tax)",
        "Manufacturer",
        "Model",
    ]), 1, inplace=True)
    df = trim_all_columns(df)
    df = df.applymap(lambda s: s.upper() if type(s) == str else s)
    df['Applicant Type'] = df.apply(lambda row: applicant_type(row), axis=1)
    df.fillna('')

    for _, row in df.iterrows():
        try:
            SpecialityUseVehicleIncentives.objects.create(
                approvals=row["Approvals"],
                date=row["Date"],
                applicant_name=row["Applicant Name"],
                max_incentive_amount_requested=row["Max Incentive Amount Requested"],
                category=row["Category"],
                applicant_type=row["Applicant Type"],
                incentive_paid=row["Incentive Paid"],
                total_purchase_price=row["Total Purchase Price (pre-tax)"],
                manufacturer=row["Manufacturer"],
                model=row["Model"],
            )
        except Exception as error:
            print(error)
            print(row)
    return True
