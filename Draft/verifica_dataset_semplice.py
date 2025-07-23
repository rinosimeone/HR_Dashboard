import pandas as pd
import numpy as np

def verifica_caratteristiche():
    """Verifica semplice delle caratteristiche del dataset."""
    
    print("🧪 VERIFICA DATASET HR REALISTICO")
    print("=" * 50)
    
    # Carica il dataset
    df = pd.read_csv('hr_data_realistico.csv')
    print(f"✅ Dataset caricato: {len(df)} dipendenti")
    
    # Converti le date
    df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], format='%m/%d/%Y')
    df['HiringDate'] = pd.to_datetime(df['HiringDate'], format='%m/%d/%Y')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp.now()
    df['Eta'] = ((oggi - df['DateOfBirth']).dt.days / 365.25).round(1)
    df['AnniServizio'] = ((oggi - df['HiringDate']).dt.days / 365.25).round(1)
    
    # TEST 1: MAGGIORANZA MASCHILE
    print(f"\n🧪 TEST 1: MAGGIORANZA MASCHILE")
    gender_counts = df['Gender'].value_counts()
    male_pct = gender_counts.get('M', 0) / len(df) * 100
    female_pct = gender_counts.get('F', 0) / len(df) * 100
    
    print(f"   • Uomini: {gender_counts.get('M', 0)} ({male_pct:.1f}%)")
    print(f"   • Donne: {gender_counts.get('F', 0)} ({female_pct:.1f}%)")
    print(f"   ✅ RISULTATO: {'SUCCESSO' if male_pct > 60 else 'PARZIALE'}")
    
    # TEST 2: PROSSIMI ALLA PENSIONE
    print(f"\n🧪 TEST 2: PROSSIMI ALLA PENSIONE")
    pensione_5_anni = len(df[df['Eta'] >= 62])
    pensione_10_anni = len(df[df['Eta'] >= 57])
    
    pct_5_anni = pensione_5_anni / len(df) * 100
    pct_10_anni = pensione_10_anni / len(df) * 100
    
    print(f"   • Pensione entro 5 anni (≥62): {pensione_5_anni} ({pct_5_anni:.1f}%)")
    print(f"   • Pensione entro 10 anni (≥57): {pensione_10_anni} ({pct_10_anni:.1f}%)")
    print(f"   ✅ RISULTATO: {'SUCCESSO' if pct_5_anni >= 15 else 'PARZIALE'}")
    
    # TEST 3: CORRELAZIONE ANZIANITÀ-STIPENDIO
    print(f"\n🧪 TEST 3: CORRELAZIONE ANZIANITÀ-STIPENDIO")
    correlazione = df['AnniServizio'].corr(df['Salary'])
    print(f"   • Correlazione: {correlazione:.3f}")
    print(f"   ✅ RISULTATO: {'SUCCESSO' if correlazione > 0.5 else 'PARZIALE'}")
    
    # TEST 4: GENDER PAY GAP
    print(f"\n🧪 TEST 4: GENDER PAY GAP")
    stipendio_medio_m = df[df['Gender'] == 'M']['Salary'].mean()
    stipendio_medio_f = df[df['Gender'] == 'F']['Salary'].mean()
    gap_percentuale = (stipendio_medio_m - stipendio_medio_f) / stipendio_medio_m * 100
    
    print(f"   • Stipendio medio uomini: €{stipendio_medio_m:,.0f}")
    print(f"   • Stipendio medio donne: €{stipendio_medio_f:,.0f}")
    print(f"   • Gap: {gap_percentuale:.1f}%")
    print(f"   ✅ RISULTATO: {'SUCCESSO' if gap_percentuale > 10 else 'PARZIALE'}")
    
    # RIEPILOGO
    print(f"\n🎯 RIEPILOGO:")
    print(f"   ✅ Maggioranza maschile: {male_pct:.1f}%")
    print(f"   ✅ Pensionamenti critici: {pct_5_anni:.1f}% entro 5 anni")
    print(f"   ✅ Correlazione anzianità-stipendio: {correlazione:.3f}")
    print(f"   ✅ Gender pay gap: {gap_percentuale:.1f}%")
    
    print(f"\n🚀 DATASET PRONTO PER L'ANALISI!")
    
    return df

if __name__ == "__main__":
    verifica_caratteristiche()
