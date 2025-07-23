"""
Modulo per l'analisi delle proiezioni pensionistiche secondo le leggi italiane.
Da integrare nel notebook HR per analisi complete.
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta

def calcola_proiezioni_pensionistiche_italia(df):
    """
    Calcola le proiezioni pensionistiche secondo le leggi italiane 2024.
    
    Parametri:
    - df: DataFrame con colonne DateOfBirth, HiringDate, Gender
    
    Restituisce:
    - DataFrame arricchito con colonne di analisi pensionistica
    """
    
    # Copia del dataframe per non modificare l'originale
    df_pensioni = df.copy()
    
    # Converti le date se necessario
    if df_pensioni['DateOfBirth'].dtype == 'object':
        df_pensioni['DateOfBirth'] = pd.to_datetime(df_pensioni['DateOfBirth'], format='%m/%d/%Y', errors='coerce')
    if df_pensioni['HiringDate'].dtype == 'object':
        df_pensioni['HiringDate'] = pd.to_datetime(df_pensioni['HiringDate'], format='%m/%d/%Y', errors='coerce')
    
    # Calcola età e anzianità attuali
    oggi = pd.Timestamp.now()
    df_pensioni['Eta'] = ((oggi - df_pensioni['DateOfBirth']).dt.days / 365.25).round(1)
    df_pensioni['AnniServizio'] = ((oggi - df_pensioni['HiringDate']).dt.days / 365.25).round(1)
    
    # LEGGI ITALIANE 2024
    # 1. Pensione di vecchiaia: 67 anni
    df_pensioni['AnniAllaPensioneVecchiaia'] = 67 - df_pensioni['Eta']
    
    # 2. Pensione anticipata: 42 anni e 10 mesi (uomini), 41 anni e 10 mesi (donne)
    # Stima anni contributivi totali (assumendo inizio lavoro a 18-22 anni)
    df_pensioni['EtaInizioLavoro'] = np.where(
        df_pensioni['Eta'] - df_pensioni['AnniServizio'] < 18, 
        18, 
        df_pensioni['Eta'] - df_pensioni['AnniServizio']
    )
    df_pensioni['AnniContributiviTotali'] = df_pensioni['Eta'] - df_pensioni['EtaInizioLavoro']
    
    # Anni contributivi necessari per pensione anticipata
    df_pensioni['AnniContributiviNecessari'] = np.where(
        df_pensioni['Gender'] == 'M', 
        42.83,  # 42 anni e 10 mesi
        41.83   # 41 anni e 10 mesi
    )
    df_pensioni['AnniAllaPensioneAnticipata'] = (
        df_pensioni['AnniContributiviNecessari'] - df_pensioni['AnniContributiviTotali']
    )
    
    # 3. Quota 103 (fino al 2024): 62 anni + 41 anni di contributi
    df_pensioni['AnniAllaQuota103_Eta'] = 62 - df_pensioni['Eta']
    df_pensioni['AnniAllaQuota103_Contributi'] = 41 - df_pensioni['AnniContributiviTotali']
    df_pensioni['AnniAllaQuota103'] = np.maximum(
        df_pensioni['AnniAllaQuota103_Eta'], 
        df_pensioni['AnniAllaQuota103_Contributi']
    )
    
    # Determina la pensione più vicina
    pensioni_possibili = df_pensioni[['AnniAllaPensioneVecchiaia', 'AnniAllaPensioneAnticipata', 'AnniAllaQuota103']]
    df_pensioni['AnniAllaPensionePiuVicina'] = pensioni_possibili.min(axis=1)
    df_pensioni['TipoPensionePiuVicina'] = pensioni_possibili.idxmin(axis=1)
    
    # Sostituisci i nomi delle colonne con nomi più leggibili
    tipo_pensione_map = {
        'AnniAllaPensioneVecchiaia': 'Vecchiaia (67 anni)',
        'AnniAllaPensioneAnticipata': 'Anticipata (contributi)',
        'AnniAllaQuota103': 'Quota 103'
    }
    df_pensioni['TipoPensionePiuVicina'] = df_pensioni['TipoPensionePiuVicina'].map(tipo_pensione_map)
    
    # Calcola anno di pensionamento
    df_pensioni['AnnoPensionamento'] = (oggi.year + df_pensioni['AnniAllaPensionePiuVicina']).round().astype(int)
    
    # Filtra solo chi può andare in pensione nei prossimi 15 anni
    df_pensioni['PuoAndareInPensione'] = df_pensioni['AnniAllaPensionePiuVicina'] <= 15
    
    return df_pensioni

def analizza_impatto_pensionistico(df_pensioni):
    """
    Analizza l'impatto delle proiezioni pensionistiche sull'azienda.
    """
    
    print("🏖️ ANALISI IMPATTO PENSIONISTICO - LEGGI ITALIANE")
    print("=" * 60)
    
    total_employees = len(df_pensioni)
    
    # 1. Distribuzione per fasce temporali
    fasce_pensione = {
        'Già in pensione': len(df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 0]),
        'Entro 1 anno': len(df_pensioni[(df_pensioni['AnniAllaPensionePiuVicina'] > 0) & (df_pensioni['AnniAllaPensionePiuVicina'] <= 1)]),
        'Entro 2-3 anni': len(df_pensioni[(df_pensioni['AnniAllaPensionePiuVicina'] > 1) & (df_pensioni['AnniAllaPensionePiuVicina'] <= 3)]),
        'Entro 4-5 anni': len(df_pensioni[(df_pensioni['AnniAllaPensionePiuVicina'] > 3) & (df_pensioni['AnniAllaPensionePiuVicina'] <= 5)]),
        'Entro 6-10 anni': len(df_pensioni[(df_pensioni['AnniAllaPensionePiuVicina'] > 5) & (df_pensioni['AnniAllaPensionePiuVicina'] <= 10)]),
        'Oltre 10 anni': len(df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] > 10])
    }
    
    print("📊 **DISTRIBUZIONE PENSIONAMENTI PER FASCE TEMPORALI:**")
    for fascia, count in fasce_pensione.items():
        pct = count / total_employees * 100
        print(f"   • {fascia}: {count} dipendenti ({pct:.1f}%)")
    
    # 2. Analisi per dipartimento (se presente)
    if 'Department' in df_pensioni.columns:
        print(f"\n🏢 **PENSIONAMENTI PER DIPARTIMENTO (Prossimi 5 anni):**")
        pensioni_5_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 5]
        if len(pensioni_5_anni) > 0:
            dept_pensioni = pensioni_5_anni['Department'].value_counts()
            for dept, count in dept_pensioni.items():
                total_dept = len(df_pensioni[df_pensioni['Department'] == dept])
                pct = count / total_dept * 100
                print(f"   • {dept}: {count}/{total_dept} dipendenti ({pct:.1f}%)")
    
    # 3. Analisi per tipo di pensione
    print(f"\n🎯 **MODALITÀ DI PENSIONAMENTO (Prossimi 10 anni):**")
    pensioni_10_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 10]
    if len(pensioni_10_anni) > 0:
        tipo_pensioni = pensioni_10_anni['TipoPensionePiuVicina'].value_counts()
        for tipo, count in tipo_pensioni.items():
            pct = count / len(pensioni_10_anni) * 100
            print(f"   • {tipo}: {count} dipendenti ({pct:.1f}%)")
    
    # 4. Impatto economico (se presente colonna Salary)
    if 'Salary' in df_pensioni.columns:
        pensioni_5_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 5]
        if len(pensioni_5_anni) > 0:
            print(f"\n💰 **IMPATTO ECONOMICO PENSIONAMENTI:**")
            stipendio_medio_pensionandi = pensioni_5_anni['Salary'].mean()
            costo_totale_5_anni = pensioni_5_anni['Salary'].sum()
            print(f"   • Stipendio medio pensionandi (5 anni): €{stipendio_medio_pensionandi:,.0f}")
            print(f"   • Costo salariale totale a rischio: €{costo_totale_5_anni:,.0f}/anno")
            print(f"   • Risparmio potenziale: €{costo_totale_5_anni:,.0f}/anno")
    
    # 5. Knowledge at risk
    pensioni_5_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 5]
    if len(pensioni_5_anni) > 0:
        anzianita_media_pensionandi = pensioni_5_anni['AnniServizio'].mean()
        print(f"\n🧠 **KNOWLEDGE AT RISK:**")
        print(f"   • Anzianità media pensionandi: {anzianita_media_pensionandi:.1f} anni")
        print(f"   • Esperienza totale a rischio: {pensioni_5_anni['AnniServizio'].sum():.0f} anni-persona")
    
    # RACCOMANDAZIONI DINAMICHE
    print(f"\n🎯 **RACCOMANDAZIONI STRATEGICHE:**")
    
    pct_pensioni_5_anni = len(pensioni_5_anni) / total_employees * 100
    
    if pct_pensioni_5_anni > 20:
        print(f"🚨 **EMERGENZA PENSIONAMENTI**: {pct_pensioni_5_anni:.1f}% va in pensione entro 5 anni!")
        print(f"   → Priorità ASSOLUTA: Piano di successione immediato")
        print(f"   → Avviare programmi di mentoring e knowledge transfer")
        print(f"   → Considerare incentivi per posticipare il pensionamento")
    elif pct_pensioni_5_anni > 10:
        print(f"⚠️  **ALTO RISCHIO**: {pct_pensioni_5_anni:.1f}% va in pensione entro 5 anni")
        print(f"   → Pianificare sostituzioni e formazione")
        print(f"   → Documentare processi critici")
    elif pct_pensioni_5_anni > 5:
        print(f"📋 **MONITORAGGIO**: {pct_pensioni_5_anni:.1f}% va in pensione entro 5 anni")
        print(f"   → Pianificazione graduale delle sostituzioni")
    else:
        print(f"✅ **SITUAZIONE STABILE**: Solo {pct_pensioni_5_anni:.1f}% va in pensione entro 5 anni")
    
    return df_pensioni

def visualizza_proiezioni_pensionistiche(df_pensioni):
    """
    Crea visualizzazioni per le proiezioni pensionistiche.
    """
    
    plt.figure(figsize=(15, 10))
    
    # Grafico 1: Distribuzione pensionamenti per anno
    plt.subplot(2, 3, 1)
    anni_pensione = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 15]['AnniAllaPensionePiuVicina'].round()
    anni_pensione.hist(bins=range(0, 16), alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Distribuzione Pensionamenti per Anno')
    plt.xlabel('Anni alla Pensione')
    plt.ylabel('Numero Dipendenti')
    plt.grid(True, alpha=0.3)
    
    # Grafico 2: Pensionamenti per dipartimento (se presente)
    if 'Department' in df_pensioni.columns:
        plt.subplot(2, 3, 2)
        pensioni_5_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 5]
        if len(pensioni_5_anni) > 0:
            dept_pensioni = pensioni_5_anni['Department'].value_counts()
            dept_pensioni.plot(kind='bar', color='coral')
            plt.title('Pensionamenti per Dipartimento (5 anni)')
            plt.xlabel('Dipartimento')
            plt.ylabel('Numero Dipendenti')
            plt.xticks(rotation=45)
    
    # Grafico 3: Tipo di pensione
    plt.subplot(2, 3, 3)
    pensioni_10_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 10]
    if len(pensioni_10_anni) > 0:
        tipo_pensioni = pensioni_10_anni['TipoPensionePiuVicina'].value_counts()
        tipo_pensioni.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Modalità di Pensionamento (10 anni)')
    
    # Grafico 4: Età vs Anni alla pensione
    plt.subplot(2, 3, 4)
    scatter_data = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 15]
    colors = scatter_data['Gender'].map({'M': 'blue', 'F': 'red'})
    plt.scatter(scatter_data['Eta'], scatter_data['AnniAllaPensionePiuVicina'], 
                c=colors, alpha=0.6)
    plt.title('Età vs Anni alla Pensione')
    plt.xlabel('Età Attuale')
    plt.ylabel('Anni alla Pensione')
    plt.legend(['Uomini', 'Donne'])
    plt.grid(True, alpha=0.3)
    
    # Grafico 5: Impatto salariale per anno (se presente)
    if 'Salary' in df_pensioni.columns:
        plt.subplot(2, 3, 5)
        impatto_annuale = []
        for anno in range(1, 11):
            pensionandi_anno = df_pensioni[
                (df_pensioni['AnniAllaPensionePiuVicina'] > anno-1) & 
                (df_pensioni['AnniAllaPensionePiuVicina'] <= anno)
            ]
            impatto_annuale.append(pensionandi_anno['Salary'].sum())
        
        plt.bar(range(1, 11), impatto_annuale, color='lightgreen', alpha=0.7)
        plt.title('Impatto Salariale per Anno')
        plt.xlabel('Anno')
        plt.ylabel('Costo Salariale (€)')
        plt.xticks(range(1, 11))
    
    # Grafico 6: Knowledge at risk
    plt.subplot(2, 3, 6)
    pensioni_5_anni = df_pensioni[df_pensioni['AnniAllaPensionePiuVicina'] <= 5]
    if len(pensioni_5_anni) > 0 and 'Salary' in df_pensioni.columns:
        plt.scatter(pensioni_5_anni['AnniServizio'], pensioni_5_anni['Salary'], 
                    c=pensioni_5_anni['AnniAllaPensionePiuVicina'], cmap='Reds', alpha=0.7)
        plt.colorbar(label='Anni alla Pensione')
        plt.title('Knowledge at Risk (5 anni)')
        plt.xlabel('Anni di Servizio')
        plt.ylabel('Stipendio (€)')
    
    plt.tight_layout()
    plt.show()

def test_modulo_pensioni():
    """Test del modulo con il dataset con turnover."""
    
    print("🧪 TEST MODULO PROIEZIONI PENSIONISTICHE")
    print("=" * 50)
    
    try:
        # Carica il dataset
        df = pd.read_csv('hr_data_con_turnover.csv')
        print(f"✅ Dataset caricato: {len(df)} dipendenti")
        
        # Filtra solo dipendenti attivi per l'analisi pensionistica
        df_attivi = df[df['EmploymentStatus'] == 'Active']
        print(f"📊 Dipendenti attivi per analisi: {len(df_attivi)}")
        
        # Calcola proiezioni pensionistiche
        df_pensioni = calcola_proiezioni_pensionistiche_italia(df_attivi)
        
        # Analizza impatto
        df_analizzato = analizza_impatto_pensionistico(df_pensioni)
        
        # Visualizza (opzionale)
        # visualizza_proiezioni_pensionistiche(df_pensioni)
        
        print(f"\n✅ Analisi pensionistica completata!")
        print(f"🎯 Modulo pronto per integrazione nel notebook!")
        
        return df_analizzato
        
    except FileNotFoundError:
        print("❌ File hr_data_con_turnover.csv non trovato!")
        print("   Esegui prima: python test_turnover_semplice.py")
        return None

if __name__ == "__main__":
    test_modulo_pensioni()
