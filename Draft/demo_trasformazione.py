import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def demo_trasformazione_insight():
    """Demo interattiva che mostra la differenza tra insight fissi e dinamici."""
    
    print("🎭 DEMO TRASFORMAZIONE: PRIMA vs DOPO")
    print("=" * 80)
    print("Confrontiamo gli insight FISSI (vecchi) con quelli DINAMICI (nuovi)")
    print("=" * 80)
    
    # Carica e prepara i dati
    df = pd.read_csv('hr_data.csv')
    
    # Converti le date
    for col in ['DateOfBirth', 'HiringDate', 'TerminationDate']:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp('2025-07-18')
    if 'DateOfBirth' in df.columns:
        eta_days = (oggi - df['DateOfBirth']).dt.days
        df['Eta'] = (eta_days / 365.25).round().astype('Int64')
    
    if 'HiringDate' in df.columns:
        servizio_days = (oggi - df['HiringDate']).dt.days
        df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')
    
    print(f"📊 Dataset caricato: {len(df)} dipendenti\n")
    
    # DEMO 1: DISTRIBUZIONE DIPARTIMENTI
    print("🏢 DEMO 1: DISTRIBUZIONE PER DIPARTIMENTI")
    print("=" * 60)
    
    print("❌ **VERSIONE VECCHIA (Insight Fissi):**")
    print("🔍 Insight:")
    print("- Il dipartimento 'Production' è il più numeroso, seguito da 'IT/IS' e 'Sales'.")
    print("- Questa visualizzazione aiuta a capire dove si concentrano le risorse umane.")
    print("  (Testo sempre uguale, anche se i dati cambiano!)")
    
    print("\n" + "-" * 60)
    print("✅ **VERSIONE NUOVA (Insight Dinamici):**")
    
    # Codice dinamico per dipartimenti
    dept_counts = df['Department'].value_counts()
    dept_percentages = (dept_counts / len(df) * 100).round(1)
    total_employees = len(df)
    
    print("🔍 **Insight Dinamici:**")
    print(f"📈 **Distribuzione per Dipartimento** (Totale: {total_employees:,} dipendenti)")
    
    # Top 3 dipartimenti
    top_3 = dept_counts.head(3)
    dept_names = list(top_3.index)
    
    print(f"\n🥇 **Top 3 Dipartimenti:**")
    for i, (dept, count) in enumerate(top_3.items(), 1):
        percentage = dept_percentages[dept]
        print(f"   {i}. **{dept}**: {count:,} dipendenti ({percentage}%)")
    
    # Analisi automatica
    largest_dept = dept_names[0]
    largest_count = top_3.iloc[0]
    largest_pct = dept_percentages.iloc[0]
    
    print(f"\n💡 **Analisi Automatica:**")
    print(f"• Il dipartimento **{largest_dept}** è il più numeroso con {largest_count:,} dipendenti ({largest_pct}% del totale)")
    
    if len(dept_names) >= 2:
        second_dept = dept_names[1]
        second_pct = dept_percentages.iloc[1]
        print(f"• Seguito da **{second_dept}** ({second_pct}%)")
        
        if len(dept_names) >= 3:
            third_dept = dept_names[2]
            third_pct = dept_percentages.iloc[2]
            print(f"• E **{third_dept}** ({third_pct}%)")
    
    # Raccomandazioni dinamiche
    print(f"\n🎯 **Raccomandazioni HR:**")
    if largest_pct > 40:
        print(f"⚠️  **Concentrazione elevata**: {largest_dept} rappresenta oltre il 40% della forza lavoro")
        print(f"   → Considerare diversificazione delle competenze e riduzione del rischio operativo")
    elif largest_pct > 30:
        print(f"📊 **Distribuzione bilanciata**: {largest_dept} ha una presenza significativa ma non eccessiva")
    else:
        print(f"✅ **Distribuzione equilibrata**: Nessun dipartimento domina eccessivamente")
    
    # Analisi dipartimenti piccoli
    small_depts = dept_counts[dept_counts < (total_employees * 0.05)]  # Meno del 5%
    if len(small_depts) > 0:
        print(f"\n🔍 **Dipartimenti piccoli** (< 5% del totale):")
        for dept, count in small_depts.items():
            pct = dept_percentages[dept]
            print(f"   • {dept}: {count} dipendenti ({pct}%)")
        print(f"   → Valutare se necessitano di rinforzi o ristrutturazione")
    
    # DEMO 2: DISTRIBUZIONE ETÀ
    print("\n\n👥 DEMO 2: DISTRIBUZIONE PER ETÀ")
    print("=" * 60)
    
    eta_media = df['Eta'].mean()
    eta_mediana = df['Eta'].median()
    
    print("❌ **VERSIONE VECCHIA (Insight Fissi):**")
    print("🔍 Insight:")
    print(f"- L'età media dei dipendenti è di {eta_media:.1f} anni.")
    print("- La maggior parte della forza lavoro si concentra nella fascia d'età 30-45 anni.")
    print("- Questa informazione è cruciale per la pianificazione della successione.")
    print("  (Sempre lo stesso testo generico!)")
    
    print("\n" + "-" * 60)
    print("✅ **VERSIONE NUOVA (Insight Dinamici):**")
    
    # Codice dinamico per età
    eta_min = df['Eta'].min()
    eta_max = df['Eta'].max()
    
    # Analisi per fasce d'età
    fasce_eta = {
        'Giovani (< 30)': len(df[df['Eta'] < 30]),
        'Adulti (30-45)': len(df[(df['Eta'] >= 30) & (df['Eta'] <= 45)]),
        'Senior (46-55)': len(df[(df['Eta'] >= 46) & (df['Eta'] <= 55)]),
        'Esperti (> 55)': len(df[df['Eta'] > 55])
    }
    
    print("🔍 **Insight Dinamici - Distribuzione per Età:**")
    print(f"📊 **Statistiche Età** (Totale: {len(df):,} dipendenti)")
    print(f"   • 📈 Età media: {eta_media:.1f} anni")
    print(f"   • 📊 Età mediana: {eta_mediana:.1f} anni")
    print(f"   • 📏 Range: {eta_min}-{eta_max} anni")
    
    print(f"\n👥 **Distribuzione per Fasce d'Età:**")
    for fascia, count in fasce_eta.items():
        pct = count / len(df) * 100
        print(f"   • {fascia}: {count:,} dipendenti ({pct:.1f}%)")
    
    # Analisi automatica della composizione
    fascia_dominante = max(fasce_eta.items(), key=lambda x: x[1])
    pct_dominante = fascia_dominante[1] / len(df) * 100
    
    print(f"\n💡 **Analisi Composizione Anagrafica:**")
    print(f"• **Fascia dominante**: {fascia_dominante[0]} con {fascia_dominante[1]:,} dipendenti ({pct_dominante:.1f}%)")
    
    # Raccomandazioni basate sui dati
    print(f"\n🎯 **Raccomandazioni HR:**")
    
    # Analisi pensionamenti
    prossimi_pensionamenti = fasce_eta['Esperti (> 55)']
    if prossimi_pensionamenti > len(df) * 0.15:  # Più del 15%
        print(f"⚠️  **Rischio pensionamenti**: {prossimi_pensionamenti} dipendenti over 55 ({prossimi_pensionamenti/len(df)*100:.1f}%)")
        print(f"   → Priorità assoluta: pianificazione successione e knowledge transfer")
    elif prossimi_pensionamenti > 0:
        print(f"📋 **Monitorare pensionamenti**: {prossimi_pensionamenti} dipendenti over 55")
        print(f"   → Pianificare gradualmente la successione")
    else:
        print(f"✅ **Nessun rischio pensionamenti immediato**: Forza lavoro giovane")
    
    # Analisi giovani talenti
    giovani = fasce_eta['Giovani (< 30)']
    if giovani < len(df) * 0.15:  # Meno del 15%
        print(f"📈 **Carenza giovani talenti**: Solo {giovani} dipendenti under 30 ({giovani/len(df)*100:.1f}%)")
        print(f"   → Intensificare recruiting junior e programmi graduate")
    else:
        print(f"✅ **Buon mix generazionale**: {giovani} giovani dipendenti ({giovani/len(df)*100:.1f}%)")
    
    # RIEPILOGO FINALE
    print("\n\n🎉 RIEPILOGO DELLA TRASFORMAZIONE")
    print("=" * 80)
    print("✅ **Vantaggi degli Insight Dinamici:**")
    print("• 📊 **Dati sempre aggiornati**: Nessun testo obsoleto")
    print("• 🎯 **Raccomandazioni specifiche**: Basate sui dati reali")
    print("• 🔍 **Identificazione automatica**: Pattern e anomalie")
    print("• 📈 **Analisi professionale**: Percentuali e statistiche precise")
    print("• 🔄 **Scalabilità**: Funziona con qualsiasi dataset")
    print("• ⚡ **Efficienza**: Riduce il lavoro manuale")
    
    print("\n🚀 **Il notebook è ora un vero strumento di Business Intelligence!**")
    
    return df

if __name__ == "__main__":
    df = demo_trasformazione_insight()
    print(f"\n📋 **Dataset utilizzato**: {len(df)} dipendenti, {len(df.columns)} colonne")
