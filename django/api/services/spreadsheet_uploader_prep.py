def prepare_arc_project_tracking(df):
    df['Publicly Announced'] = df['Publicly Announced'].replace({'No': False, 'N': False, 'Yes': True, 'Y': True})
    return df

