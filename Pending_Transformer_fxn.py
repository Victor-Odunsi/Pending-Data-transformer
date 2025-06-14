import pandas as pd
import re

def Pending_transformer(filepath, sheet_name = 'Sheet1'):
    
    df = pd.read_excel(filepath, sheet_name = sheet_name)

    df.columns = df.columns.str.strip()
    
    columns = ['PENDING TEST', 'TEST ORDERED', 'STATUS', 'RECEIVED  LOCATION']
    df = df[columns]

    df.dropna(inplace = True)

    df['TEST ORDERED'] = df['TEST ORDERED'].str.strip()
    
    chem_keys = [
        r'U/E+CR', 'UREA', 'LIPASE', 'E/U/CR', 'LIPO', 'FBS', 'GGT', 'CAL', 'PO4', 'LFT', 'SOD', 'CRP', 'LIPOGRAM', 'CREAT', 'S',
        'CHOL', 'CKMM', 'CR', 'POT', 'ELEC', 'ALK', 'UA', 'CPK', 'MAG', 'CRP', 'LDH', 'BILIRUBIN', 'AFP', 'AMYL', 'GLU',
        'GLOBULIN', 'TOT PROT', 'ALB', 'GGT', 'ALDOLASE', 'ALT', 'AST', 'TBIL', 'ANION', 'DBIL', 'TRIG', 'IRON', 'CO2', 'URE', 'GLUCOSE',
        'VIT', 'ANTI-MULLERIAN', 'TESTO', 'T3', 'T4', 'CA153', 'PSA', 'bHCG', 'QHCG', 'E2', 'FOL', 'PROG', 'FSH', 'LH', 'PROL', 'TSH',
        'THY', 'CA125', 'TRANSF', 'SAT', 'FERR', 'CORT', 'CEA', 'CA19-9'
    ]

    haem_keys = [
        'FBC', 'RETIC', 'GENOTYPE', 'BLOOD', 'COOMBS', 'HBAIC', 'ESR', 'MALARIA', 'RETICULOCYTES', 'APTT', 'PI', 'INR', 'QUANTIFERONE',
        'Hct', 'HCT', 'TROPONIN', 'TROPO', 'DIMER', 'PLATELETS', 'NORMOBLASTS', 'CKMB', 'MICROFILARIA', 'MP'
    ]

    sero_keys = [
        'RPR', 'WIDAL', 'RAPID', 'HIV', 'HEP', r'H.PYLORI', 'HAM', 'bHCG', 'IgM'
    ]
    
    def classify(test_name):
        for key in sero_keys:
            match = re.search(key, test_name, re.IGNORECASE)
            if match:
                return 'serology'

        for key in haem_keys:
            match = re.search(key, test_name, re.IGNORECASE)
            if match:
                return 'haematology'

        for key in chem_keys:
            match = re.search(key, test_name, re.IGNORECASE)
            if match:
                return 'chemistry'

        return 'Others'
    
    df['TEST CATEGORY'] = df['TEST ORDERED'].apply(lambda test: classify(test))
    
    return df

Update made to .py file