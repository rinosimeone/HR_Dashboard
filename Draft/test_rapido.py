import pandas as pd
import numpy as np

print("🧪 TEST RAPIDO SISTEMA HR")
print("=" * 30)

# Test caricamento dataset
df = pd.read_csv('hr_data_con_turnover.csv')
print(f"✅ Dataset: {len(df)} dipendenti")

# Test distribuzione status
status = df['EmploymentStatus'].value_counts()
print(f"📊 Status: {status.to_dict()}")

# Test turnover per genere
df_attivi = df[df['EmploymentStatus'] == 'Active']
df_usciti = df[df['EmploymentStatus'] == 'Terminated']

m_total = len(df[df['Gender'] == 'M'])
f_total = len(df[df['Gender'] == 'F'])
m_usciti = len(df_usciti[df_usciti['Gender'] == 'M'])
f_usciti = len(df_usciti[df_usciti['Gender'] == 'F'])

turnover_m = m_usciti / m_total * 100
turnover_f = f_usciti / f_total * 100
gap = turnover_f - turnover_m

print(f"🔄 Turnover M: {turnover_m:.1f}%")
print(f"🔄 Turnover F: {turnover_f:.1f}%")
print(f"⚖️ Gap: {gap:.1f} punti")

# Test insight dinamico
if gap > 30:
    print("🚨 EMERGENZA TURNOVER FEMMINILE!")
elif gap > 20:
    print("⚠️ ALTO RISCHIO")
else:
    print("📊 SITUAZIONE NORMALE")

print("✅ SISTEMA FUNZIONANTE!")
