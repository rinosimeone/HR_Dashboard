"""
Crea un dashboard corretto con KPI in alto e risolve il problema df.
"""

# Setup iniziale
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import warnings
warnings.filterwarnings('ignore')

# Configurazione grafici
plt.style.use('default')
sns.set_palette('viridis')
plt.rcParams['figure.figsize'] = (12, 8)

print('📊 HR Analytics Dashboard - Setup completato!')

# 📁 CARICAMENTO DATI HR
def carica_dati_hr():
    """Carica e prepara i dati HR per l'analisi."""
    
    try:
        # Prova prima il dataset con turnover
        df = pd.read_csv('hr_data_con_turnover.csv')
        print(f"✅ Dataset con turnover caricato: {len(df)} dipendenti")
        dataset_type = "turnover"
    except FileNotFoundError:
        try:
            # Fallback al dataset originale
            df = pd.read_csv('hr_data.csv')
            print(f"✅ Dataset originale caricato: {len(df)} dipendenti")
            dataset_type = "originale"
        except FileNotFoundError:
            print("❌ Nessun dataset trovato!")
            return None, None
    
    # Converti le date
    date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp.now()
    if 'DateOfBirth' in df.columns:
        eta_days = (oggi - df['DateOfBirth']).dt.days
        df['Eta'] = (eta_days / 365.25).round().astype('Int64')
    
    if 'HiringDate' in df.columns:
        servizio_days = (oggi - df['HiringDate']).dt.days
        df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')
        df['AnnoAssunzione'] = df['HiringDate'].dt.year
    
    print(f"📊 Dati preparati per l'analisi!")
    return df, dataset_type

# Carica i dati
df, dataset_type = carica_dati_hr()

# 🎯 KPI PRINCIPALI - INDICATORI CHIAVE
if df is not None:
    print("\n🎯 HR DASHBOARD - KPI PRINCIPALI")
    print("=" * 50)
    
    df_analisi = df[df['EmploymentStatus'] == 'Active'] if 'EmploymentStatus' in df.columns else df
    total_employees = len(df_analisi)
    
    print(f"👥 **WORKFORCE ATTIVA**: {total_employees:,} dipendenti")
    
    # KPI 1: Turnover Rate
    if 'EmploymentStatus' in df.columns:
        df_usciti = df[df['EmploymentStatus'] == 'Terminated']
        turnover_rate = len(df_usciti) / len(df) * 100
        status_icon = "🚨" if turnover_rate > 25 else "⚠️" if turnover_rate > 15 else "✅"
        print(f"\n🔄 **TURNOVER RATE**: {turnover_rate:.1f}% {status_icon}")
        
        # Gender gap turnover
        if 'Gender' in df.columns:
            m_total = len(df[df['Gender'] == 'M'])
            f_total = len(df[df['Gender'] == 'F'])
            m_usciti = len(df_usciti[df_usciti['Gender'] == 'M'])
            f_usciti = len(df_usciti[df_usciti['Gender'] == 'F'])
            
            if m_total > 0 and f_total > 0:
                turnover_m = m_usciti / m_total * 100
                turnover_f = f_usciti / f_total * 100
                gap = turnover_f - turnover_m
                gap_icon = "🚨" if abs(gap) > 20 else "⚠️" if abs(gap) > 10 else "✅"
                print(f"   • Gender Gap: {gap:.1f} punti {gap_icon}")
    
    # KPI 2: Gender Balance
    if 'Gender' in df_analisi.columns:
        gender_counts = df_analisi['Gender'].value_counts()
        male_pct = gender_counts.get('M', 0) / total_employees * 100
        female_pct = gender_counts.get('F', 0) / total_employees * 100
        balance_gap = abs(male_pct - female_pct)
        balance_icon = "🚨" if balance_gap > 30 else "⚠️" if balance_gap > 20 else "✅"
        print(f"\n⚖️ **GENDER BALANCE**: {male_pct:.0f}%M / {female_pct:.0f}%F {balance_icon}")
    
    # KPI 3: Pay Gap
    if 'Salary' in df_analisi.columns and 'Gender' in df_analisi.columns:
        salary_by_gender = df_analisi.groupby('Gender')['Salary'].mean()
        if 'M' in salary_by_gender.index and 'F' in salary_by_gender.index:
            pay_gap = (salary_by_gender['M'] - salary_by_gender['F']) / salary_by_gender['M'] * 100
            pay_icon = "🚨" if pay_gap > 20 else "⚠️" if pay_gap > 10 else "✅"
            print(f"\n💰 **PAY GAP**: {pay_gap:.1f}% {pay_icon}")
    
    # KPI 4: Age Risk
    if 'Eta' in df_analisi.columns:
        eta_media = df_analisi['Eta'].mean()
        over_60 = len(df_analisi[df_analisi['Eta'] >= 60])
        risk_pct = over_60 / total_employees * 100
        age_icon = "🚨" if risk_pct > 20 else "⚠️" if risk_pct > 15 else "✅"
        print(f"\n🏖️ **RETIREMENT RISK**: {risk_pct:.1f}% over 60 {age_icon}")
        print(f"   • Età media: {eta_media:.1f} anni")
    
    # KPI 5: Performance
    if 'PerformanceScore' in df_analisi.columns:
        top_perf = len(df_analisi[df_analisi['PerformanceScore'] == 'Exceeds'])
        top_pct = top_perf / total_employees * 100
        perf_icon = "✅" if top_pct > 15 else "⚠️" if top_pct > 10 else "🚨"
        print(f"\n📈 **TOP PERFORMERS**: {top_pct:.1f}% {perf_icon}")
    
    print(f"\n🎯 **STATUS GENERALE**: ", end="")
    # Conta gli alert
    alerts = 0
    if 'EmploymentStatus' in df.columns and turnover_rate > 25: alerts += 1
    if 'Gender' in df_analisi.columns and balance_gap > 30: alerts += 1
    if 'Salary' in df_analisi.columns and 'Gender' in df_analisi.columns and pay_gap > 20: alerts += 1
    if 'Eta' in df_analisi.columns and risk_pct > 20: alerts += 1
    
    if alerts >= 3:
        print("🚨 SITUAZIONE CRITICA - Azione immediata richiesta")
    elif alerts >= 1:
        print("⚠️ ATTENZIONE - Monitoraggio attivo necessario")
    else:
        print("✅ SITUAZIONE STABILE - Mantenere standard attuali")

print("\n" + "="*60)
print("📋 MODULI SPECIALIZZATI DISPONIBILI:")
print("   🔄 03_Analisi_Turnover.ipynb - Analisi turnover critico")
print("   🏖️ 04_Proiezioni_Pensionistiche.ipynb - Pianificazione pensioni")
print("   💰 02_Analisi_Retributiva.ipynb - Pay gap analysis")
print("   👥 01_Analisi_Demografica.ipynb - Composizione workforce")
print("   📈 05_Performance_Analysis.ipynb - Talent management")
print("   📋 06_Report_Esecutivo.ipynb - Dashboard leadership")
print("="*60)
