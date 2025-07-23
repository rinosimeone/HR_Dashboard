import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Genera dataset semplice con alto turnover femminile
print("🔄 Generazione Dataset con Alto Turnover Femminile")

# Parametri
np.random.seed(42)
random.seed(42)

n_attivi = 150
n_usciti = 100

# Dipendenti attivi: 70% M, 30% F
attivi_m = 105
attivi_f = 45

# Dipendenti usciti: 25% M, 75% F (ALTO TURNOVER FEMMINILE!)
usciti_m = 25
usciti_f = 75

# Crea liste
all_data = []

# ID counter
emp_id = 1

# Dipendenti attivi
for i in range(attivi_m):
    all_data.append({
        'EmployeeID': emp_id,
        'EmployeeName': f'Marco Rossi {emp_id}',
        'Gender': 'M',
        'EmploymentStatus': 'Active',
        'Salary': random.randint(30000, 60000),
        'Department': random.choice(['Produzione', 'IT', 'Vendite', 'Amministrazione']),
        'DateOfBirth': f'01/01/{random.randint(1960, 1990)}',
        'HiringDate': f'01/01/{random.randint(2010, 2020)}',
        'TerminationDate': ''
    })
    emp_id += 1

for i in range(attivi_f):
    all_data.append({
        'EmployeeID': emp_id,
        'EmployeeName': f'Giulia Bianchi {emp_id}',
        'Gender': 'F',
        'EmploymentStatus': 'Active',
        'Salary': random.randint(25000, 50000),  # Gender pay gap
        'Department': random.choice(['Produzione', 'IT', 'Vendite', 'Amministrazione']),
        'DateOfBirth': f'01/01/{random.randint(1960, 1990)}',
        'HiringDate': f'01/01/{random.randint(2010, 2020)}',
        'TerminationDate': ''
    })
    emp_id += 1

# Dipendenti usciti
for i in range(usciti_m):
    all_data.append({
        'EmployeeID': emp_id,
        'EmployeeName': f'Antonio Verdi {emp_id}',
        'Gender': 'M',
        'EmploymentStatus': 'Terminated',
        'Salary': random.randint(28000, 55000),
        'Department': random.choice(['Produzione', 'IT', 'Vendite', 'Amministrazione']),
        'DateOfBirth': f'01/01/{random.randint(1960, 1990)}',
        'HiringDate': f'01/01/{random.randint(2015, 2020)}',
        'TerminationDate': f'01/01/{random.randint(2022, 2024)}'
    })
    emp_id += 1

for i in range(usciti_f):
    all_data.append({
        'EmployeeID': emp_id,
        'EmployeeName': f'Sara Neri {emp_id}',
        'Gender': 'F',
        'EmploymentStatus': 'Terminated',
        'Salary': random.randint(22000, 45000),  # Gender pay gap ancora più evidente
        'Department': random.choice(['Vendite', 'Amministrazione', 'Marketing', 'HR']),
        'DateOfBirth': f'01/01/{random.randint(1960, 1990)}',
        'HiringDate': f'01/01/{random.randint(2015, 2020)}',
        'TerminationDate': f'01/01/{random.randint(2022, 2024)}'
    })
    emp_id += 1

# Crea DataFrame
df = pd.DataFrame(all_data)

# Aggiungi colonne mancanti
df['State'] = 'IT'
df['MaritalStatus'] = 'Married'
df['Position'] = 'Impiegato'
df['RecruitmentSource'] = 'LinkedIn'
df['PerformanceScore'] = 'Fully Meets'

# Salva
df.to_csv('hr_data_con_turnover.csv', index=False)

print(f"✅ Dataset generato: {len(df)} dipendenti totali")

# Analisi rapida
df_attivi = df[df['EmploymentStatus'] == 'Active']
df_usciti = df[df['EmploymentStatus'] == 'Terminated']

print(f"\n📊 DIPENDENTI ATTIVI:")
print(f"   • Uomini: {len(df_attivi[df_attivi['Gender'] == 'M'])}")
print(f"   • Donne: {len(df_attivi[df_attivi['Gender'] == 'F'])}")

print(f"\n📊 DIPENDENTI USCITI:")
print(f"   • Uomini: {len(df_usciti[df_usciti['Gender'] == 'M'])}")
print(f"   • Donne: {len(df_usciti[df_usciti['Gender'] == 'F'])}")

# Calcola turnover
totale_m = len(df[df['Gender'] == 'M'])
totale_f = len(df[df['Gender'] == 'F'])
usciti_m_count = len(df_usciti[df_usciti['Gender'] == 'M'])
usciti_f_count = len(df_usciti[df_usciti['Gender'] == 'F'])

turnover_m = usciti_m_count / totale_m * 100
turnover_f = usciti_f_count / totale_f * 100

print(f"\n🔄 TASSO TURNOVER:")
print(f"   • Uomini: {turnover_m:.1f}%")
print(f"   • Donne: {turnover_f:.1f}%")
print(f"   • Differenza: {turnover_f - turnover_m:.1f} punti percentuali")

print(f"\n🚨 ALTO TURNOVER FEMMINILE CONFERMATO!")
print(f"💾 File salvato: hr_data_con_turnover.csv")
