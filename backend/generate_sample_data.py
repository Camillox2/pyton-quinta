"""1. Execute: python generate_sample_data.py
"""

import pandas as pd
import numpy as np
from pathlib import Path
import sys

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')
    sys.stderr = codecs.getwriter('utf-8')(sys.stderr.buffer, 'strict')


def generate_sample_mental_health_data(n_samples=1000):
    np.random.seed(42)
    
    genders = ['Male', 'Female', 'Non-binary', 'Prefer not to say']
    countries = [
        'United States', 'United Kingdom', 'Canada', 'Australia', 'Germany', 
        'India', 'Brazil', 'France', 'Japan', 'Mexico', 'Spain', 'Italy', 
        'South Africa', 'Argentina', 'Netherlands', 'Sweden', 'South Korea', 
        'China', 'Russia', 'Turkey', 'Poland', 'Belgium', 'Switzerland', 
        'Portugal', 'Greece', 'Denmark', 'Norway', 'Finland', 'Ireland', 'Austria'
    ]
    occupations = ['Software Engineer', 'Teacher', 'Healthcare Worker', 'Student',
                   'Business Analyst', 'Designer', 'Manager', 'Sales']
    yes_no = ['Yes', 'No']
    mood_levels = ['Low', 'Medium', 'High', 'Very High']
    
    data = {
        'Gender': np.random.choice(genders, n_samples),
        'Country': np.random.choice(countries, n_samples),
        'Occupation': np.random.choice(occupations, n_samples),
        'SelfEmployed': np.random.choice(yes_no, n_samples),
        'FamilyHistory': np.random.choice(yes_no, n_samples),
        'DaysIndoors': np.random.randint(0, 8, n_samples),
        'HabitsChange': np.random.choice(yes_no, n_samples),
        'CopingStruggles': np.random.choice(yes_no, n_samples),
        'MentalHealthHistory': np.random.choice(yes_no, n_samples),
        'IncreasingStress': np.random.choice(yes_no, n_samples),
        'MoodSwings': np.random.choice(mood_levels, n_samples),
        'WorkInterest': np.random.choice(['Low', 'Medium', 'High'], n_samples),
        'SocialWeakness': np.random.choice(yes_no, n_samples),
        'MentalHealthInterview': np.random.choice(yes_no, n_samples),
        'CareOptions': np.random.choice(yes_no, n_samples),
        'NeedSupport': np.random.choice(yes_no, n_samples)
    }
    
    df = pd.DataFrame(data)
    
    for col in df.columns:
        if np.random.random() > 0.7:
            missing_indices = np.random.choice(df.index, size=int(0.05 * n_samples), replace=False)
            df.loc[missing_indices, col] = np.nan
    
    return df


def main():
    print("Gerando dados de exemplo...")
    
    data_dir = Path(__file__).parent / 'data'
    data_dir.mkdir(exist_ok=True)
    
    df = generate_sample_mental_health_data(n_samples=1000)
    
    output_path = data_dir / 'sample_mental_health_data.csv'
    df.to_csv(output_path, index=False)
    
    print(f"Dados de exemplo gerados com sucesso!")
    print(f"Arquivo salvo em: {output_path}")
    print(f"Número de amostras: {len(df)}")
    print(f"Número de colunas: {len(df.columns)}")
    print(f"\nPrimeiras linhas:")
    print(df.head())
    print(f"\nInformações do dataset:")
    print(df.info())


if __name__ == "__main__":
    main()
