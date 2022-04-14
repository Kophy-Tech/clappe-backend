import pandas as pd
import numpy as np

def get_data():

    '''
    This function is for extracting the neccessary data from the file.
    It returns a tuple of dict containing the extracted data.

    Input: None
    Output: tuple of dict for patient access, coding, claims and financial services, exactly in that order.
    '''

    data = pd.read_excel("app/pdf/JC_Dashboard_Data.xlsx")

    # sauce code: 222359

    # extract those belonging to Patient Access category and group them based on the metric
    patient_access = data[data['Category'] == 'Patient Access']
    patient_access_group = patient_access.groupby('Metrics')


    patient_access_data = ['Pre-Registration Rate ',
                            'Insurance Verification Rate',
                            'Service Authorization Rate- Inpatient (IP) & OBS',
                            'Service Authorization Rate- Outpatient (OP)',
                            'Conversion Rate % of Uninsured Patient to 3rd Party Insurance (Funding Source) ',
                            'Point-of-Service (POS) Cash Collections ']


    patient_access_dict = {}
    for i in ['Current', 'Target', 'HFMA', 'EPIC']:
        # find the mean aggregate of each group
        patient_access_group_single = patient_access_group[i].aggregate(np.mean)
        patient_access_dict[i] = {}

        # extract the value for the needed metrics
        for item in patient_access_data:
            patient_access_dict[i][item] = round(patient_access_group_single[item], 2)


# sauce code: 151436

# extract those belonging to Coding category and group them based on metric
    coding =  data[data['Category'] == 'Coding ']
    coding_group = coding.groupby('Metrics')

    coding_data = ['Days in Total Discharged Not Final Billed (DNFB)',
                    'Days in Total Discharged Not Submitted to Payor (DNSP)',
                    'Days in Final Bill Not Submitted to Payer (FBNS)',
                    'Total Charge Lag Days ',
                    'Case Mix Index ']

    coding_dict = {}
    for i in ['Current', 'Target', 'HFMA', 'EPIC']:
        # find the mean aggregate of each group
        coding_single = coding_group[i].aggregate(np.mean)
        coding_dict[i] = {}

        # extract the value for the needed metrics
        for item in coding_data:
            coding_dict[i][item] = round(coding_single[item], 2)




# sauce code: 79930

# extract those belonging to Claims category and group them based on metric
    claims =  data[data['Category'] == 'Claims ']
    claims_group = claims.groupby('Metrics')

    claims_data = ['Clean Claims Rate ', 'Late charges (as % of Total charges) ']

    claims_dict = {}
    for i in ['Current', 'Target', 'HFMA', 'EPIC']:
        # find the mean aggregate of each group
        claims_single = claims_group[i].aggregate(np.mean)
        claims_dict[i] = {}

        # extract the value for the needed metrics
        for item in claims_data:
            claims_dict[i][item] = round(claims_single[item], 2)


# sauce code: 87114
# extract those belonging to Patient Financial Service category and group them based on metric
    patient_financial = data[data['Category'] == 'Patient Financial Services ']
    financial_group = patient_financial.groupby('Metrics')

    financial_data = ['Aged AR as a % of Total Billed AR',
                        'Aged AR as a % of Total AR ',
                        'Net Days In AR',
                        'Cash Collections as % of NPSR',
                        'Uncompensated Care ',
                        'Point-of-Service (POS) Cash Collections ',
                        'Remittance Denials Rate ',
                        'Denial Write-offs as a % of NPSR',
                        'Bad Debt',
                        'Charity Care',
                        'Net Days in Credit Balance',
                        'cost to Collect ']

    financial_dict = {}
    for i in ['Current', 'Target', 'HFMA', 'EPIC']:
        # find the mean aggregate of each group
        financial_single = financial_group[i].aggregate(np.mean)
        financial_dict[i] = {}

        # extract the value for the needed metrics
        for item in financial_data:
            financial_dict[i][item] = round(financial_single[item], 2)



# sauce code: 151436

    # return the tuple of dict containing the extracted data
    return patient_access_dict, coding_dict, claims_dict, financial_dict