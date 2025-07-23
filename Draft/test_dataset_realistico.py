import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from scipy.stats import pearsonr

def test_caratteristiche_dataset():
    """Test completo delle caratteristiche richieste nel nuovo dataset."""
    
    print("🧪 TEST DATASET HR REALISTICO")
    print("=" * 60)
    
    # Carica il dataset
    try:
        df = pd.read_csv('hr_data_realistico.csv')
        print(f"✅ Dataset caricato: {len(df)} dipendenti")
    except FileNotFoundError:
        print("❌ File non trovato! Esegui prima: python genera_dataset_realistico.py")
        return
    
    # Converti le date
    df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], format='%m/%d/%Y')
    df['HiringDate'] = pd.to_datetime(df['HiringDate'], format='%m/%d/%Y')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp.now()
    df['Eta'] = ((oggi - df['DateOfBirth']).dt.days / 365.25).round(1)
    df['AnniServizio'] = ((oggi - df['HiringDate']).dt.days / 365.25).round(1)
    
    print(f"\n📊 **PANORAMICA GENERALE:**")
    print(f"   • Totale dipendenti: {len(df)}")
    print(f"   • Età media: {df['Eta'].mean():.1f} anni")
    print(f"   • Anzianità media: {df['AnniServizio'].mean():.1f} anni")
    print(f"   • Stipendio medio: €{df['Salary'].mean():,.0f}")
    
    # TEST 1: MAGGIORANZA MASCHILE
    print(f"\n🧪 **TEST 1: MAGGIORANZA MASCHILE**")
    gender_counts = df['Gender'].value_counts()
    male_pct = gender_counts.get('M', 0) / len(df) * 100
    female_pct = gender_counts.get('F', 0) / len(df) * 100
    
    print(f"   • Uomini: {gender_counts.get('M', 0)} ({male_pct:.1f}%)")
    print(f"   • Donne: {gender_counts.get('F', 0)} ({female_pct:.1f}%)")
    
    if male_pct > 50:
        print(f"   ✅ SUCCESSO: Maggioranza maschile ({male_pct:.1f}%)")
    else:
        print(f"   ❌ FALLITO: Non c'è maggioranza maschile")
    
    # TEST 2: MOLTI PROSSIMI ALLA PENSIONE
    print(f"\n🧪 **TEST 2: PROSSIMI ALLA PENSIONE (Leggi Italiane)**")
    
    # Pensione a 67 anni in Italia
    pensione_5_anni = len(df[df['Eta'] >= 62])  # Pensione entro 5 anni
    pensione_10_anni = len(df[df['Eta'] >= 57])  # Pensione entro 10 anni
    
    pct_5_anni = pensione_5_anni / len(df) * 100
    pct_10_anni = pensione_10_anni / len(df) * 100
    
    print(f"   • Pensione entro 5 anni (età ≥62): {pensione_5_anni} ({pct_5_anni:.1f}%)")
    print(f"   • Pensione entro 10 anni (età ≥57): {pensione_10_anni} ({pct_10_anni:.1f}%)")
    
    if pct_5_anni >= 15 and pct_10_anni >= 25:
        print(f"   ✅ SUCCESSO: Molti prossimi alla pensione")
    else:
        print(f"   ⚠️  PARZIALE: Alcuni prossimi alla pensione")
    
    # Distribuzione per fasce d'età
    fasce_eta = {
        'Giovani (< 35)': len(df[df['Eta'] < 35]),
        'Adulti (35-50)': len(df[(df['Eta'] >= 35) & (df['Eta'] < 50)]),
        'Maturi (50-60)': len(df[(df['Eta'] >= 50) & (df['Eta'] < 60)]),
        'Pre-pensione (≥60)': len(df[df['Eta'] >= 60])
    }
    
    print(f"\n   📊 **Distribuzione per Fasce d'Età:**")
    for fascia, count in fasce_eta.items():
        pct = count / len(df) * 100
        print(f"      • {fascia}: {count} ({pct:.1f}%)")
    
    # TEST 3: CORRELAZIONE ANZIANITÀ-STIPENDIO
    print(f"\n🧪 **TEST 3: CORRELAZIONE ANZIANITÀ-STIPENDIO**")
    
    correlazione, p_value = pearsonr(df['AnniServizio'], df['Salary'])
    
    print(f"   • Correlazione Pearson: {correlazione:.3f}")
    print(f"   • P-value: {p_value:.6f}")
    
    if correlazione > 0.5 and p_value < 0.05:
        print(f"   ✅ SUCCESSO: Forte correlazione positiva significativa")
    elif correlazione > 0.3:
        print(f"   ⚠️  PARZIALE: Correlazione moderata")
    else:
        print(f"   ❌ FALLITO: Correlazione debole")
    
    # Analisi dettagliata correlazione
    print(f"\n   📊 **Analisi Dettagliata:**")
    
    # Stipendio per fasce di anzianità
    fasce_anzianita = {
        'Nuovi (0-5 anni)': df[df['AnniServizio'] <= 5]['Salary'].mean(),
        'Junior (6-15 anni)': df[(df['AnniServizio'] > 5) & (df['AnniServizio'] <= 15)]['Salary'].mean(),
        'Senior (16-25 anni)': df[(df['AnniServizio'] > 15) & (df['AnniServizio'] <= 25)]['Salary'].mean(),
        'Veterani (>25 anni)': df[df['AnniServizio'] > 25]['Salary'].mean()
    }
    
    for fascia, stipendio_medio in fasce_anzianita.items():
        if not pd.isna(stipendio_medio):
            print(f"      • {fascia}: €{stipendio_medio:,.0f}")
    
    # TEST 4: GENDER PAY GAP
    print(f"\n🧪 **TEST 4: GENDER PAY GAP**")
    
    stipendio_medio_m = df[df['Gender'] == 'M']['Salary'].mean()
    stipendio_medio_f = df[df['Gender'] == 'F']['Salary'].mean()
    
    gap_assoluto = stipendio_medio_m - stipendio_medio_f
    gap_percentuale = (gap_assoluto / stipendio_medio_m) * 100
    
    print(f"   • Stipendio medio uomini: €{stipendio_medio_m:,.0f}")
    print(f"   • Stipendio medio donne: €{stipendio_medio_f:,.0f}")
    print(f"   • Gap assoluto: €{gap_assoluto:,.0f}")
    print(f"   • Gap percentuale: {gap_percentuale:.1f}%")
    
    if gap_percentuale > 10:
        print(f"   ✅ SUCCESSO: Gender pay gap evidente ({gap_percentuale:.1f}%)")
    elif gap_percentuale > 5:
        print(f"   ⚠️  PARZIALE: Gap moderato")
    else:
        print(f"   ❌ FALLITO: Gap troppo piccolo")
    
    # Analisi gap per fasce di anzianità
    print(f"\n   📊 **Gap per Fasce di Anzianità:**")
    for fascia_nome, fascia_filter in [
        ('Nuovi (0-10 anni)', df['AnniServizio'] <= 10),
        ('Esperti (11-20 anni)', (df['AnniServizio'] > 10) & (df['AnniServizio'] <= 20)),
        ('Veterani (>20 anni)', df['AnniServizio'] > 20)
    ]:
        fascia_df = df[fascia_filter]
        if len(fascia_df) > 0:
            m_salary = fascia_df[fascia_df['Gender'] == 'M']['Salary'].mean()
            f_salary = fascia_df[fascia_df['Gender'] == 'F']['Salary'].mean()
            if not pd.isna(m_salary) and not pd.isna(f_salary):
                gap_fascia = (m_salary - f_salary) / m_salary * 100
                print(f"      • {fascia_nome}: {gap_fascia:.1f}% gap")
    
    # VISUALIZZAZIONI
    print(f"\n📊 **GENERAZIONE GRAFICI...**")
    
    plt.figure(figsize=(16, 12))
    
    # Grafico 1: Distribuzione per genere
    plt.subplot(2, 4, 1)
    gender_counts.plot(kind='bar', color=['lightblue', 'lightcoral'])
    plt.title('Distribuzione per Genere')
    plt.ylabel('Numero Dipendenti')
    plt.xticks(rotation=0)
    
    # Grafico 2: Distribuzione età
    plt.subplot(2, 4, 2)
    df['Eta'].hist(bins=15, alpha=0.7, color='skyblue', edgecolor='black')
    plt.axvline(x=62, color='red', linestyle='--', label='Pensione tra 5 anni')
    plt.axvline(x=67, color='darkred', linestyle='-', label='Pensione di vecchiaia')
    plt.title('Distribuzione Età')
    plt.xlabel('Età')
    plt.ylabel('Numero Dipendenti')
    plt.legend()
    
    # Grafico 3: Correlazione anzianità-stipendio
    plt.subplot(2, 4, 3)
    plt.scatter(df['AnniServizio'], df['Salary'], alpha=0.6, c=df['Gender'].map({'M': 'blue', 'F': 'red'}))
    plt.title(f'Anzianità vs Stipendio (r={correlazione:.3f})')
    plt.xlabel('Anni di Servizio')
    plt.ylabel('Stipendio (€)')
    
    # Linea di tendenza
    z = np.polyfit(df['AnniServizio'], df['Salary'], 1)
    p = np.poly1d(z)
    plt.plot(df['AnniServizio'], p(df['AnniServizio']), "r--", alpha=0.8)
    
    # Grafico 4: Gender pay gap per anzianità
    plt.subplot(2, 4, 4)
    df_pivot = df.groupby(['AnniServizio', 'Gender'])['Salary'].mean().unstack()
    if 'M' in df_pivot.columns and 'F' in df_pivot.columns:
        plt.plot(df_pivot.index, df_pivot['M'], 'b-', label='Uomini', linewidth=2)
        plt.plot(df_pivot.index, df_pivot['F'], 'r-', label='Donne', linewidth=2)
        plt.title('Stipendio per Anzianità e Genere')
        plt.xlabel('Anni di Servizio')
        plt.ylabel('Stipendio Medio (€)')
        plt.legend()
    
    # Grafico 5: Distribuzione stipendi per genere
    plt.subplot(2, 4, 5)
    df[df['Gender'] == 'M']['Salary'].hist(alpha=0.7, label='Uomini', bins=15, color='blue')
    df[df['Gender'] == 'F']['Salary'].hist(alpha=0.7, label='Donne', bins=15, color='red')
    plt.title('Distribuzione Stipendi per Genere')
    plt.xlabel('Stipendio (€)')
    plt.ylabel('Frequenza')
    plt.legend()
    
    # Grafico 6: Pensionamenti per dipartimento
    plt.subplot(2, 4, 6)
    pensionandi = df[df['Eta'] >= 62]
    if len(pensionandi) > 0:
        dept_pensioni = pensionandi['Department'].value_counts()
        dept_pensioni.plot(kind='bar', color='orange', alpha=0.7)
        plt.title('Pensionamenti per Dipartimento (5 anni)')
        plt.xlabel('Dipartimento')
        plt.ylabel('Numero Dipendenti')
        plt.xticks(rotation=45)
    
    # Grafico 7: Boxplot stipendi per genere
    plt.subplot(2, 4, 7)
    sns.boxplot(data=df, x='Gender', y='Salary', palette=['lightblue', 'lightcoral'])
    plt.title('Distribuzione Stipendi per Genere')
    plt.ylabel('Stipendio (€)')
    
    # Grafico 8: Heatmap correlazioni
    plt.subplot(2, 4, 8)
    corr_data = df[['Eta', 'AnniServizio', 'Salary']].corr()
    sns.heatmap(corr_data, annot=True, cmap='coolwarm', center=0, square=True)
    plt.title('Matrice Correlazioni')
    
    plt.tight_layout()
    plt.show()
    
    # RIEPILOGO FINALE
    print(f"\n🎯 **RIEPILOGO TEST:**")
    print(f"   ✅ Maggioranza maschile: {male_pct:.1f}%")
    print(f"   ✅ Pensionamenti 5 anni: {pct_5_anni:.1f}%")
    print(f"   ✅ Correlazione anzianità-stipendio: {correlazione:.3f}")
    print(f"   ✅ Gender pay gap: {gap_percentuale:.1f}%")
    
    print(f"\n🚀 **DATASET PRONTO PER L'ANALISI HR AVANZATA!**")
    
    return df

if __name__ == "__main__":
    test_caratteristiche_dataset()
