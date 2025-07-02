import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt

class PendingTransformer():
    def __init__(self):
        pass

    def wrangle(self, filepath, sheet_name = 'Sheet1'):
        
        columns = ['PENDING TEST', 'TEST ORDERED', 'COL DATE', 'RECEIVED LOCATION']
    
        df = pd.read_excel(filepath, sheet_name = sheet_name)
        for col in columns:
            if col not in df.columns:
                raise Exception(f'{col} not in Datafame columns')
    
        df.columns = df.columns.str.strip()
        
        columns = ['PENDING TEST', 'TEST ORDERED', 'COL DATE', 'RECEIVED LOCATION']
        df = df[columns]
    
        df.dropna(inplace = True)
    
        df['TEST ORDERED'] = df['TEST ORDERED'].str.strip()
    
        chem_keys = [
            r'U/E+CR', 'UREA', 'LIPASE', 'E/U/CR', 'LIPO', 'FBS', 'CAL', 'PO4', 'LFT', 'SOD', 'CRP', 'LIPOGRAM', 'CREAT',
            'CHOL', 'CKMM', 'CR', 'POT', 'ELEC', 'ALK', 'UA', 'CPK', 'MAG', 'CRP', 'LDH', 'BILIRUBIN', 'AFP', 'AMYL', 'GLU',
            'GLOBULIN', 'TOT PROT', 'ALB', 'GGT', 'ALDOLASE', 'ALT', 'AST', 'TBIL', 'ANION', 'DBIL', 'TRIG', 'IRON', 'CO2', 'URE', 'GLUCOSE',
            'VIT', 'ANTI-MULLERIAN', 'TESTO', 'T3', 'T4', 'CA153', 'PSA', 'bHCG', 'QHCG', 'E2', 'FOL', 'PROG', 'FSH', 'LH', 'PROL', 'TSH',
            'THY', 'CA125', 'TRANSF', 'SAT', 'FERR', 'CORT', 'CEA', 'CA19-9'
        ]
    
        haem_keys = [
            'FBC', 'RETIC', 'GENOTYPE', 'BLOOD', 'COOMBS', 'HBAIC', 'ESR', 'Hb ELECT', 'MALARIA', 'RETICULOCYTES', 'APTT', 'PI', 'INR', 'QUANTIFERONE',
            'Hct', 'HCT', 'TROPONIN', 'TROPO', 'DIMER', 'PLATELETS', 'NORMOBLASTS', 'CKMB', 'MICROFILARIA', 'MP'
        ]
    
        sero_keys = [
            'RPR', 'WIDAL', 'HIV', 'HEP', r'H.PYLORI', 'HAM', 'bHCG', 'IgM', 'HEP C', 'HEP B', 'HIV'
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
                
            return 'others'
        
        df['TEST CATEGORY'] = df['TEST ORDERED'].apply(lambda test: classify(test))
    
        return df
    
    def build_charts(self, filepath):
        df = self.wrangle(filepath)
        dist = df.groupby('RECEIVED LOCATION')['PENDING TEST'].count()
        sns.set_theme()
        fig, ax = plt.subplots(figsize = (5,4))
        sns.barplot(
            data = dist,
            width =0.8,
            ax = ax,
        )
        plt.xlabel('Location')
        plt.ylabel('Count of pending samples')
        plt.title('Distribution of Pending samples')
        ax.bar_label(ax.containers[0], fmt='%d', padding=3);
    
        locs = df['RECEIVED LOCATION'].unique()
    
        location_dfs = {loc: df[df['RECEIVED LOCATION'] == loc] for loc in locs}
    
        for loc, subdf in location_dfs.items():
            # Group by TEST CATEGORY and count PENDING TESTS
            test_counts = subdf.groupby('TEST CATEGORY')['PENDING TEST'].count().reset_index()
            
            # Create the plot
            fig, ax = plt.subplots(figsize=(10, 5))
            sns.barplot(
                data=test_counts,
                x='PENDING TEST',
                y='TEST CATEGORY',
                hue = 'TEST CATEGORY',
                orient = 'h',
                palette='viridis',
                width = 0.5
            )
            
            # Customize the plot
            plt.title(f'Pending Tests by Category - {loc}')
            plt.xlabel('Test Category')
            plt.ylabel('Count of Pending Tests')
            
            # Add value labels on bars
            for container in ax.containers:
                ax.bar_label(container, fmt='%d', padding=3)
            
            plt.tight_layout()
            plt.show()