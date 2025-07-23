import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import numpy as np

def analisi_proiezioni_pensionistiche_italia(df):
    """
    Analisi completa delle proiezioni pensionistiche secondo le leggi italiane.
    
    Leggi italiane 2024:
    - Pensione di vecchiaia: 67 anni
    - Pensione anticipata: 42 anni e 10 mesi di contributi (uomini), 41 anni e 10 mesi (donne)
    - Quota 103: 62 anni + 41 anni di contributi (fino al 2024)
    """
    
    print("🏖️ ANALISI PROIEZIONI PENSIONISTICHE - LEGGI ITALIANE")
    print("=" * 70)
    
    # Converti le date se necessario
    if df['DateOfBirth'].dtype == 'object':
        df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], format='%m/%d/%Y', errors='coerce')
    if df['HiringDate'].dtype == 'object':
        df['HiringDate'] = pd.to_datetime(df['HiringDate'], format='%m/%d/%Y', errors='coerce')
    
    # Calcola età e anzianità attuali
    oggi = pd.Timestamp.now()
    df['Eta'] = ((oggi - df['DateOfBirth']).dt.days / 365.25).round(1)
    df['AnniServizio'] = ((oggi - df['HiringDate']).dt.days / 365.25).round(1)
    
    # Calcola anni alla pensione secondo diverse modalità
    df['AnniAllaPensioneVecchiaia'] = 67 - df['Eta']  # Pensione di vecchiaia
    
    # Pensione anticipata (assumiamo che abbiano iniziato a lavorare a 18-22 anni)
    # Stima anni contributivi totali (non solo in azienda)
    df['EtaInizioLavoro'] = np.where(df['Eta'] - df['AnniServizio'] < 18, 18, df['Eta'] - df['AnniServizio'])
    df['AnniContributiviTotali'] = df['Eta'] - df['EtaInizioLavoro']
    
    # Anni alla pensione anticipata
    df['AnniContributiviNecessari'] = np.where(df['Gender'] == 'M', 42.83, 41.83)  # 42a10m uomini, 41a10m donne
    df['AnniAllaPensioneAnticipata'] = df['AnniContributiviNecessari'] - df['AnniContributiviTotali']
    
    # Quota 103 (62 anni + 41 anni contributi)
    df['AnniAllaQuota103_Eta'] = 62 - df['Eta']
    df['AnniAllaQuota103_Contributi'] = 41 - df['AnniContributiviTotali']
    df['AnniAllaQuota103'] = np.maximum(df['AnniAllaQuota103_Eta'], df['AnniAllaQuota103_Contributi'])
    
    # Determina la pensione più vicina
    df['AnniAllaPensionePiuVicina'] = df[['AnniAllaPensioneVecchiaia', 'AnniAllaPensioneAnticipata', 'AnniAllaQuota103']].min(axis=1)
    df['TipoPensionePiuVicina'] = df[['AnniAllaPensioneVecchiaia', 'AnniAllaPensioneAnticipata', 'AnniAllaQuota103']].idxmin(axis=1)
    
    # Sostituisci i nomi delle colonne con nomi più leggibili
    df['TipoPensionePiuVicina'] = df['TipoPensionePiuVicina'].map({
        'AnniAllaPensioneVecchiaia': 'Vecchiaia (67 anni)',
        'AnniAllaPensioneAnticipata': 'Anticipata (contributi)',
        'AnniAllaQuota103': 'Quota 103'
    })
    
    # Filtra solo chi può andare in pensione (anni positivi o molto vicini)
    df['PuoAndareInPensione'] = df['AnniAllaPensionePiuVicina'] <= 15  # Prossimi 15 anni
    
    # ANALISI E VISUALIZZAZIONI
    
    # 1. Distribuzione per fasce temporali
    fasce_pensione = {
        'Già in pensione': len(df[df['AnniAllaPensionePiuVicina'] <= 0]),
        'Entro 1 anno': len(df[(df['AnniAllaPensionePiuVicina'] > 0) & (df['AnniAllaPensionePiuVicina'] <= 1)]),
        'Entro 2-3 anni': len(df[(df['AnniAllaPensionePiuVicina'] > 1) & (df['AnniAllaPensionePiuVicina'] <= 3)]),
        'Entro 4-5 anni': len(df[(df['AnniAllaPensionePiuVicina'] > 3) & (df['AnniAllaPensionePiuVicina'] <= 5)]),
        'Entro 6-10 anni': len(df[(df['AnniAllaPensionePiuVicina'] > 5) & (df['AnniAllaPensionePiuVicina'] <= 10)]),
        'Oltre 10 anni': len(df[df['AnniAllaPensionePiuVicina'] > 10])
    }
    
    print("📊 **DISTRIBUZIONE PENSIONAMENTI PER FASCE TEMPORALI:**")
    total_employees = len(df)
    for fascia, count in fasce_pensione.items():
        pct = count / total_employees * 100
        print(f"   • {fascia}: {count} dipendenti ({pct:.1f}%)")
    
    # 2. Analisi per dipartimento
    print(f"\n🏢 **PENSIONAMENTI PER DIPARTIMENTO (Prossimi 5 anni):**")
    pensioni_5_anni = df[df['AnniAllaPensionePiuVicina'] <= 5]
    if len(pensioni_5_anni) > 0:
        dept_pensioni = pensioni_5_anni['Department'].value_counts()
        for dept, count in dept_pensioni.items():
            total_dept = len(df[df['Department'] == dept])
            pct = count / total_dept * 100
            print(f"   • {dept}: {count}/{total_dept} dipendenti ({pct:.1f}%)")
    
    # 3. Analisi per tipo di pensione
    print(f"\n🎯 **MODALITÀ DI PENSIONAMENTO (Prossimi 10 anni):**")
    pensioni_10_anni = df[df['AnniAllaPensionePiuVicina'] <= 10]
    if len(pensioni_10_anni) > 0:
        tipo_pensioni = pensioni_10_anni['TipoPensionePiuVicina'].value_counts()
        for tipo, count in tipo_pensioni.items():
            pct = count / len(pensioni_10_anni) * 100
            print(f"   • {tipo}: {count} dipendenti ({pct:.1f}%)")
    
    # 4. Impatto economico
    print(f"\n💰 **IMPATTO ECONOMICO PENSIONAMENTI:**")
    if len(pensioni_5_anni) > 0:
        stipendio_medio_pensionandi = pensioni_5_anni['Salary'].mean()
        costo_totale_5_anni = pensioni_5_anni['Salary'].sum()
        print(f"   • Stipendio medio pensionandi (5 anni): €{stipendio_medio_pensionandi:,.0f}")
        print(f"   • Costo salariale totale a rischio: €{costo_totale_5_anni:,.0f}/anno")
        print(f"   • Risparmio potenziale: €{costo_totale_5_anni:,.0f}/anno")
    
    # 5. Knowledge at risk
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
    
    # Raccomandazioni per dipartimenti critici
    if len(pensioni_5_anni) > 0:
        dept_critici = dept_pensioni[dept_pensioni / df['Department'].value_counts() > 0.15]
        if len(dept_critici) > 0:
            print(f"\n🏢 **DIPARTIMENTI CRITICI** (>15% pensionamenti):")
            for dept in dept_critici.index:
                print(f"   • {dept}: Pianificare urgentemente le sostituzioni")
    
    # VISUALIZZAZIONI
    plt.figure(figsize=(15, 12))
    
    # Grafico 1: Distribuzione pensionamenti per anno
    plt.subplot(2, 3, 1)
    anni_pensione = df[df['AnniAllaPensionePiuVicina'] <= 15]['AnniAllaPensionePiuVicina'].round()
    anni_pensione.hist(bins=range(0, 16), alpha=0.7, color='skyblue', edgecolor='black')
    plt.title('Distribuzione Pensionamenti per Anno')
    plt.xlabel('Anni alla Pensione')
    plt.ylabel('Numero Dipendenti')
    plt.grid(True, alpha=0.3)
    
    # Grafico 2: Pensionamenti per dipartimento
    plt.subplot(2, 3, 2)
    if len(pensioni_5_anni) > 0:
        dept_pensioni.plot(kind='bar', color='coral')
        plt.title('Pensionamenti per Dipartimento (5 anni)')
        plt.xlabel('Dipartimento')
        plt.ylabel('Numero Dipendenti')
        plt.xticks(rotation=45)
    
    # Grafico 3: Tipo di pensione
    plt.subplot(2, 3, 3)
    if len(pensioni_10_anni) > 0:
        tipo_pensioni.plot(kind='pie', autopct='%1.1f%%', startangle=90)
        plt.title('Modalità di Pensionamento (10 anni)')
    
    # Grafico 4: Età vs Anni alla pensione
    plt.subplot(2, 3, 4)
    scatter_data = df[df['AnniAllaPensionePiuVicina'] <= 15]
    plt.scatter(scatter_data['Eta'], scatter_data['AnniAllaPensionePiuVicina'], 
                c=scatter_data['Gender'].map({'M': 'blue', 'F': 'red'}), alpha=0.6)
    plt.title('Età vs Anni alla Pensione')
    plt.xlabel('Età Attuale')
    plt.ylabel('Anni alla Pensione')
    plt.legend(['Uomini', 'Donne'])
    plt.grid(True, alpha=0.3)
    
    # Grafico 5: Impatto salariale per anno
    plt.subplot(2, 3, 5)
    impatto_annuale = []
    for anno in range(1, 11):
        pensionandi_anno = df[(df['AnniAllaPensionePiuVicina'] > anno-1) & (df['AnniAllaPensionePiuVicina'] <= anno)]
        impatto_annuale.append(pensionandi_anno['Salary'].sum())
    
    plt.bar(range(1, 11), impatto_annuale, color='lightgreen', alpha=0.7)
    plt.title('Impatto Salariale per Anno')
    plt.xlabel('Anno')
    plt.ylabel('Costo Salariale (€)')
    plt.xticks(range(1, 11))
    
    # Grafico 6: Knowledge at risk
    plt.subplot(2, 3, 6)
    if len(pensioni_5_anni) > 0:
        plt.scatter(pensioni_5_anni['AnniServizio'], pensioni_5_anni['Salary'], 
                    c=pensioni_5_anni['AnniAllaPensionePiuVicina'], cmap='Reds', alpha=0.7)
        plt.colorbar(label='Anni alla Pensione')
        plt.title('Knowledge at Risk (5 anni)')
        plt.xlabel('Anni di Servizio')
        plt.ylabel('Stipendio (€)')
    
    plt.tight_layout()
    plt.show()
    
    return df

def test_analisi_pensioni():
    """Test dell'analisi pensionistica con il nuovo dataset."""
    print("🧪 Test Analisi Proiezioni Pensionistiche")
    print("=" * 50)
    
    # Carica il dataset realistico
    try:
        df = pd.read_csv('hr_data_realistico.csv')
        print(f"✅ Dataset caricato: {len(df)} dipendenti")
        
        # Esegui l'analisi
        df_analizzato = analisi_proiezioni_pensionistiche_italia(df)
        
        print(f"\n💾 Analisi completata!")
        return df_analizzato
        
    except FileNotFoundError:
        print("❌ File hr_data_realistico.csv non trovato!")
        print("   Esegui prima: python genera_dataset_realistico.py")
        return None

if __name__ == "__main__":
    test_analisi_pensioni()
