import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from datetime import datetime, timedelta

def analisi_turnover_completa():
    """Analisi completa del turnover con focus sul gender gap."""
    
    print("🔄 ANALISI TURNOVER DETTAGLIATA")
    print("=" * 50)
    
    # Carica il dataset
    try:
        df = pd.read_csv('hr_data_con_turnover.csv')
        print(f"✅ Dataset caricato: {len(df)} dipendenti totali")
    except FileNotFoundError:
        print("❌ File non trovato! Esegui prima: python genera_dataset_con_turnover.py")
        return
    
    # Converti le date
    df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], format='%m/%d/%Y')
    df['HiringDate'] = pd.to_datetime(df['HiringDate'], format='%m/%d/%Y')
    df['TerminationDate'] = pd.to_datetime(df['TerminationDate'], format='%m/%d/%Y', errors='coerce')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp.now()
    df['Eta'] = ((oggi - df['DateOfBirth']).dt.days / 365.25).round(1)
    df['AnniServizio'] = ((oggi - df['HiringDate']).dt.days / 365.25).round(1)
    
    # Separa dipendenti attivi e usciti
    df_attivi = df[df['EmploymentStatus'] == 'Active']
    df_usciti = df[df['EmploymentStatus'] == 'Terminated']
    
    print(f"\n📊 **PANORAMICA GENERALE:**")
    print(f"   • Dipendenti attivi: {len(df_attivi)}")
    print(f"   • Dipendenti usciti: {len(df_usciti)}")
    print(f"   • Tasso turnover globale: {len(df_usciti)/len(df)*100:.1f}%")
    
    # ANALISI TURNOVER PER GENERE
    print(f"\n👥 **ANALISI TURNOVER PER GENERE:**")
    
    # Dipendenti attivi per genere
    attivi_m = len(df_attivi[df_attivi['Gender'] == 'M'])
    attivi_f = len(df_attivi[df_attivi['Gender'] == 'F'])
    
    # Dipendenti usciti per genere
    usciti_m = len(df_usciti[df_usciti['Gender'] == 'M'])
    usciti_f = len(df_usciti[df_usciti['Gender'] == 'F'])
    
    # Calcola tassi di turnover
    totale_m = attivi_m + usciti_m
    totale_f = attivi_f + usciti_f
    
    turnover_rate_m = usciti_m / totale_m * 100
    turnover_rate_f = usciti_f / totale_f * 100
    
    print(f"   🚹 **UOMINI:**")
    print(f"      • Attivi: {attivi_m}")
    print(f"      • Usciti: {usciti_m}")
    print(f"      • Tasso turnover: {turnover_rate_m:.1f}%")
    
    print(f"   🚺 **DONNE:**")
    print(f"      • Attive: {attivi_f}")
    print(f"      • Uscite: {usciti_f}")
    print(f"      • Tasso turnover: {turnover_rate_f:.1f}%")
    
    print(f"   ⚖️  **GENDER GAP TURNOVER: {turnover_rate_f - turnover_rate_m:.1f} punti percentuali**")
    
    # ANALISI PER DIPARTIMENTO
    print(f"\n🏢 **TURNOVER PER DIPARTIMENTO:**")
    dept_analysis = []
    
    for dept in df['Department'].unique():
        dept_df = df[df['Department'] == dept]
        dept_attivi = len(dept_df[dept_df['EmploymentStatus'] == 'Active'])
        dept_usciti = len(dept_df[dept_df['EmploymentStatus'] == 'Terminated'])
        dept_totale = dept_attivi + dept_usciti
        dept_turnover = dept_usciti / dept_totale * 100 if dept_totale > 0 else 0
        
        dept_analysis.append({
            'Dipartimento': dept,
            'Attivi': dept_attivi,
            'Usciti': dept_usciti,
            'Turnover%': dept_turnover
        })
    
    dept_df_analysis = pd.DataFrame(dept_analysis).sort_values('Turnover%', ascending=False)
    
    for _, row in dept_df_analysis.head().iterrows():
        print(f"   • {row['Dipartimento']}: {row['Usciti']}/{row['Attivi']+row['Usciti']} ({row['Turnover%']:.1f}%)")
    
    # ANALISI TEMPORALE TURNOVER
    print(f"\n📅 **ANALISI TEMPORALE:**")
    if len(df_usciti) > 0:
        # Calcola durata media del servizio per chi ha lasciato
        df_usciti['DurataServizio'] = (df_usciti['TerminationDate'] - df_usciti['HiringDate']).dt.days / 365.25
        
        durata_media_m = df_usciti[df_usciti['Gender'] == 'M']['DurataServizio'].mean()
        durata_media_f = df_usciti[df_usciti['Gender'] == 'F']['DurataServizio'].mean()
        
        print(f"   • Durata media servizio uomini usciti: {durata_media_m:.1f} anni")
        print(f"   • Durata media servizio donne uscite: {durata_media_f:.1f} anni")
        print(f"   • Differenza: {durata_media_m - durata_media_f:.1f} anni")
    
    # ANALISI CORRELAZIONE STIPENDIO-TURNOVER
    print(f"\n💰 **CORRELAZIONE STIPENDIO-TURNOVER:**")
    stipendio_medio_usciti = df_usciti['Salary'].mean()
    stipendio_medio_attivi = df_attivi['Salary'].mean()
    
    print(f"   • Stipendio medio chi è rimasto: €{stipendio_medio_attivi:,.0f}")
    print(f"   • Stipendio medio chi ha lasciato: €{stipendio_medio_usciti:,.0f}")
    print(f"   • Differenza: €{stipendio_medio_attivi - stipendio_medio_usciti:,.0f}")
    
    # ANALISI PER FASCE DI ETÀ
    print(f"\n👶 **TURNOVER PER FASCE DI ETÀ:**")
    fasce_eta = [
        ('Giovani (< 35)', df['Eta'] < 35),
        ('Adulti (35-50)', (df['Eta'] >= 35) & (df['Eta'] < 50)),
        ('Maturi (≥ 50)', df['Eta'] >= 50)
    ]
    
    for nome_fascia, filtro in fasce_eta:
        fascia_df = df[filtro]
        if len(fascia_df) > 0:
            fascia_attivi = len(fascia_df[fascia_df['EmploymentStatus'] == 'Active'])
            fascia_usciti = len(fascia_df[fascia_df['EmploymentStatus'] == 'Terminated'])
            fascia_totale = fascia_attivi + fascia_usciti
            fascia_turnover = fascia_usciti / fascia_totale * 100 if fascia_totale > 0 else 0
            print(f"   • {nome_fascia}: {fascia_usciti}/{fascia_totale} ({fascia_turnover:.1f}%)")
    
    # RACCOMANDAZIONI DINAMICHE
    print(f"\n🎯 **RACCOMANDAZIONI URGENTI:**")
    
    if turnover_rate_f > 50:
        print(f"🚨 **EMERGENZA TURNOVER FEMMINILE**: {turnover_rate_f:.1f}% delle donne ha lasciato l'azienda!")
        print(f"   → Azione immediata: Exit interview approfondite")
        print(f"   → Revisione politiche di work-life balance")
        print(f"   → Analisi cultura aziendale e inclusività")
    elif turnover_rate_f > 30:
        print(f"⚠️  **ALTO RISCHIO TURNOVER FEMMINILE**: {turnover_rate_f:.1f}%")
        print(f"   → Programmi di retention specifici per donne")
        print(f"   → Mentoring e career development")
    
    if turnover_rate_f - turnover_rate_m > 20:
        print(f"⚖️  **GENDER GAP CRITICO**: {turnover_rate_f - turnover_rate_m:.1f} punti di differenza")
        print(f"   → Analisi pay equity urgente")
        print(f"   → Revisione processi di promozione")
        print(f"   → Programmi di leadership femminile")
    
    # Dipartimenti critici
    dept_critici = dept_df_analysis[dept_df_analysis['Turnover%'] > 40]
    if len(dept_critici) > 0:
        print(f"\n🏢 **DIPARTIMENTI IN CRISI** (turnover > 40%):")
        for _, row in dept_critici.iterrows():
            print(f"   • {row['Dipartimento']}: {row['Turnover%']:.1f}% turnover")
        print(f"   → Intervento manageriale immediato necessario")
    
    # VISUALIZZAZIONI
    print(f"\n📊 **GENERAZIONE GRAFICI...**")
    
    plt.figure(figsize=(16, 12))
    
    # Grafico 1: Turnover per genere
    plt.subplot(2, 4, 1)
    turnover_data = [turnover_rate_m, turnover_rate_f]
    colors = ['lightblue', 'lightcoral']
    plt.bar(['Uomini', 'Donne'], turnover_data, color=colors)
    plt.title('Tasso di Turnover per Genere')
    plt.ylabel('Turnover (%)')
    for i, v in enumerate(turnover_data):
        plt.text(i, v + 1, f'{v:.1f}%', ha='center', fontweight='bold')
    
    # Grafico 2: Distribuzione dipendenti per status e genere
    plt.subplot(2, 4, 2)
    status_gender = df.groupby(['EmploymentStatus', 'Gender']).size().unstack()
    status_gender.plot(kind='bar', stacked=True, color=['lightblue', 'lightcoral'])
    plt.title('Dipendenti per Status e Genere')
    plt.ylabel('Numero Dipendenti')
    plt.xticks(rotation=45)
    plt.legend(['Uomini', 'Donne'])
    
    # Grafico 3: Turnover per dipartimento
    plt.subplot(2, 4, 3)
    dept_df_analysis.head(6).plot(x='Dipartimento', y='Turnover%', kind='bar', color='orange', alpha=0.7)
    plt.title('Turnover per Dipartimento')
    plt.ylabel('Turnover (%)')
    plt.xticks(rotation=45)
    
    # Grafico 4: Durata servizio per genere (usciti)
    plt.subplot(2, 4, 4)
    if len(df_usciti) > 0:
        df_usciti.boxplot(column='DurataServizio', by='Gender', ax=plt.gca())
        plt.title('Durata Servizio per Genere (Usciti)')
        plt.ylabel('Anni di Servizio')
        plt.suptitle('')  # Rimuove il titolo automatico
    
    # Grafico 5: Stipendio vs Status
    plt.subplot(2, 4, 5)
    df.boxplot(column='Salary', by='EmploymentStatus', ax=plt.gca())
    plt.title('Stipendio per Status')
    plt.ylabel('Stipendio (€)')
    plt.suptitle('')
    
    # Grafico 6: Età vs Turnover
    plt.subplot(2, 4, 6)
    df_usciti['Eta'].hist(alpha=0.7, label='Usciti', bins=15, color='red')
    df_attivi['Eta'].hist(alpha=0.7, label='Attivi', bins=15, color='blue')
    plt.title('Distribuzione Età: Attivi vs Usciti')
    plt.xlabel('Età')
    plt.ylabel('Frequenza')
    plt.legend()
    
    # Grafico 7: Turnover nel tempo (per mese di uscita)
    plt.subplot(2, 4, 7)
    if len(df_usciti) > 0:
        df_usciti['MeseUscita'] = df_usciti['TerminationDate'].dt.month
        monthly_exits = df_usciti['MeseUscita'].value_counts().sort_index()
        monthly_exits.plot(kind='line', marker='o', color='red')
        plt.title('Uscite per Mese')
        plt.xlabel('Mese')
        plt.ylabel('Numero Uscite')
    
    # Grafico 8: Heatmap turnover per dipartimento e genere
    plt.subplot(2, 4, 8)
    pivot_data = df.groupby(['Department', 'Gender', 'EmploymentStatus']).size().unstack(fill_value=0)
    if 'Terminated' in pivot_data.columns:
        turnover_by_dept_gender = pivot_data['Terminated'] / (pivot_data.sum(axis=1)) * 100
        turnover_matrix = turnover_by_dept_gender.unstack(level=1, fill_value=0)
        sns.heatmap(turnover_matrix, annot=True, fmt='.1f', cmap='Reds')
        plt.title('Turnover % per Dipartimento e Genere')
    
    plt.tight_layout()
    plt.show()
    
    print(f"\n🚨 **SITUAZIONE CRITICA CONFERMATA!**")
    print(f"   • Turnover femminile: {turnover_rate_f:.1f}%")
    print(f"   • Gender gap turnover: {turnover_rate_f - turnover_rate_m:.1f} punti")
    print(f"   • Azione immediata richiesta!")
    
    return df

if __name__ == "__main__":
    analisi_turnover_completa()
