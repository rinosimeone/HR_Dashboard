"""
Script per popolare il modulo di analisi turnover con contenuto completo.
"""

import json

def crea_cella_codice(codice):
    """Crea una cella di codice."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": codice.split('\n')
    }

def crea_cella_markdown(testo):
    """Crea una cella markdown."""
    return {
        "cell_type": "markdown", 
        "metadata": {},
        "source": testo.split('\n')
    }

def popola_modulo_turnover():
    """Popola il modulo di analisi turnover."""
    
    print("🔄 Popolamento Modulo Analisi Turnover...")
    
    # Carica il notebook esistente
    with open('03_Analisi_Turnover.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Rimuovi il placeholder
    notebook["cells"] = notebook["cells"][:3]  # Mantieni solo header, setup e import
    
    # Sezione 1: Analisi Turnover Generale
    notebook["cells"].append(crea_cella_markdown("""
## 🔄 Analisi Turnover Generale

Analisi completa dei tassi di turnover con focus particolare sul gender gap.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 🔄 ANALISI TURNOVER GENERALE
if df is not None:
    print("🔄 ANALISI TURNOVER E RETENTION")
    print("=" * 50)
    
    # Separa dipendenti attivi e usciti
    if 'EmploymentStatus' in df.columns:
        df_attivi = df[df['EmploymentStatus'] == 'Active']
        df_usciti = df[df['EmploymentStatus'] == 'Terminated']
        
        print(f"👥 **Panoramica Generale:**")
        print(f"   • Dipendenti attivi: {len(df_attivi):,}")
        print(f"   • Dipendenti usciti: {len(df_usciti):,}")
        print(f"   • Tasso turnover globale: {len(df_usciti)/len(df)*100:.1f}%")
        
        # Analisi per genere
        if 'Gender' in df.columns:
            print(f"\\n👥 **TURNOVER PER GENERE:**")
            
            # Calcola tassi per genere
            for gender in ['M', 'F']:
                gender_label = "Uomini" if gender == 'M' else "Donne"
                
                attivi_gender = len(df_attivi[df_attivi['Gender'] == gender])
                usciti_gender = len(df_usciti[df_usciti['Gender'] == gender])
                totale_gender = attivi_gender + usciti_gender
                
                if totale_gender > 0:
                    turnover_rate = usciti_gender / totale_gender * 100
                    print(f"   🚹🚺 **{gender_label}:**")
                    print(f"      • Attivi: {attivi_gender:,}")
                    print(f"      • Usciti: {usciti_gender:,}")
                    print(f"      • Tasso turnover: {turnover_rate:.1f}%")
            
            # Calcola gender gap turnover
            m_total = len(df[df['Gender'] == 'M'])
            f_total = len(df[df['Gender'] == 'F'])
            m_usciti = len(df_usciti[df_usciti['Gender'] == 'M'])
            f_usciti = len(df_usciti[df_usciti['Gender'] == 'F'])
            
            if m_total > 0 and f_total > 0:
                turnover_m = m_usciti / m_total * 100
                turnover_f = f_usciti / f_total * 100
                gap = turnover_f - turnover_m
                
                print(f"\\n⚖️  **GENDER GAP TURNOVER: {gap:.1f} punti percentuali**")
                
                if gap > 20:
                    print(f"🚨 **EMERGENZA**: Turnover femminile critico!")
                elif gap > 10:
                    print(f"⚠️  **ALTO RISCHIO**: Significativo gap di genere")
                elif gap > 5:
                    print(f"📋 **MONITORAGGIO**: Gap moderato da tenere sotto controllo")
                else:
                    print(f"✅ **EQUILIBRATO**: Gap contenuto")
    else:
        print("ℹ️  Dataset non contiene informazioni su turnover")
        print("   Analisi limitata ai dipendenti attuali")
"""))
    
    # Sezione 2: Analisi per Dipartimento
    notebook["cells"].append(crea_cella_markdown("""
## 🏢 Turnover per Dipartimento

Identificazione dei dipartimenti con maggiori problemi di retention.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 🏢 ANALISI TURNOVER PER DIPARTIMENTO
if df is not None and 'EmploymentStatus' in df.columns and 'Department' in df.columns:
    
    print("🏢 TURNOVER PER DIPARTIMENTO")
    print("=" * 40)
    
    # Analisi per ogni dipartimento
    dept_analysis = []
    
    for dept in df['Department'].unique():
        dept_df = df[df['Department'] == dept]
        dept_attivi = len(dept_df[dept_df['EmploymentStatus'] == 'Active'])
        dept_usciti = len(dept_df[dept_df['EmploymentStatus'] == 'Terminated'])
        dept_totale = dept_attivi + dept_usciti
        
        if dept_totale > 0:
            dept_turnover = dept_usciti / dept_totale * 100
            
            dept_analysis.append({
                'Dipartimento': dept,
                'Attivi': dept_attivi,
                'Usciti': dept_usciti,
                'Totale': dept_totale,
                'Turnover%': dept_turnover
            })
    
    # Ordina per turnover decrescente
    dept_analysis.sort(key=lambda x: x['Turnover%'], reverse=True)
    
    print("📊 **Classifica Turnover per Dipartimento:**")
    for i, dept in enumerate(dept_analysis, 1):
        status_icon = "🚨" if dept['Turnover%'] > 40 else "⚠️" if dept['Turnover%'] > 25 else "📋" if dept['Turnover%'] > 15 else "✅"
        print(f"   {i:2d}. {status_icon} {dept['Dipartimento']}: {dept['Usciti']}/{dept['Totale']} ({dept['Turnover%']:.1f}%)")
    
    # Identifica dipartimenti critici
    dept_critici = [d for d in dept_analysis if d['Turnover%'] > 40]
    if dept_critici:
        print(f"\\n🚨 **DIPARTIMENTI IN CRISI** (turnover > 40%):")
        for dept in dept_critici:
            print(f"   • {dept['Dipartimento']}: {dept['Turnover%']:.1f}% turnover")
        print(f"   → Intervento manageriale URGENTE necessario")
    
    # Raccomandazioni per dipartimenti
    print(f"\\n🎯 **RACCOMANDAZIONI PER DIPARTIMENTO:**")
    for dept in dept_analysis[:3]:  # Top 3 con più turnover
        if dept['Turnover%'] > 25:
            print(f"   • **{dept['Dipartimento']}** ({dept['Turnover%']:.1f}%):")
            print(f"     → Exit interview approfondite")
            print(f"     → Revisione management e cultura del team")
            print(f"     → Programmi di retention specifici")
"""))
    
    # Sezione 3: Visualizzazioni
    notebook["cells"].append(crea_cella_markdown("""
## 📊 Visualizzazioni Turnover

Grafici per comprendere meglio i pattern di turnover.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 📊 VISUALIZZAZIONI TURNOVER
if df is not None and 'EmploymentStatus' in df.columns:
    
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('Analisi Turnover - Dashboard Visuale', fontsize=16, fontweight='bold')
    
    # Grafico 1: Turnover per genere
    if 'Gender' in df.columns:
        turnover_data = []
        labels = []
        
        for gender in ['M', 'F']:
            gender_total = len(df[df['Gender'] == gender])
            gender_usciti = len(df[(df['Gender'] == gender) & (df['EmploymentStatus'] == 'Terminated')])
            if gender_total > 0:
                turnover_rate = gender_usciti / gender_total * 100
                turnover_data.append(turnover_rate)
                labels.append('Uomini' if gender == 'M' else 'Donne')
        
        colors = ['lightblue', 'lightcoral']
        bars = axes[0,0].bar(labels, turnover_data, color=colors)
        axes[0,0].set_title('Tasso di Turnover per Genere')
        axes[0,0].set_ylabel('Turnover (%)')
        
        # Aggiungi valori sulle barre
        for bar, value in zip(bars, turnover_data):
            axes[0,0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 1, 
                          f'{value:.1f}%', ha='center', fontweight='bold')
    
    # Grafico 2: Status dipendenti
    status_counts = df['EmploymentStatus'].value_counts()
    axes[0,1].pie(status_counts.values, labels=status_counts.index, autopct='%1.1f%%', 
                  startangle=90, colors=['lightgreen', 'lightcoral'])
    axes[0,1].set_title('Distribuzione Status Dipendenti')
    
    # Grafico 3: Turnover per dipartimento
    if 'Department' in df.columns:
        dept_turnover = {}
        for dept in df['Department'].unique():
            dept_total = len(df[df['Department'] == dept])
            dept_usciti = len(df[(df['Department'] == dept) & (df['EmploymentStatus'] == 'Terminated')])
            if dept_total > 0:
                dept_turnover[dept] = dept_usciti / dept_total * 100
        
        # Ordina e prendi top 6
        sorted_depts = sorted(dept_turnover.items(), key=lambda x: x[1], reverse=True)[:6]
        dept_names = [d[0] for d in sorted_depts]
        dept_rates = [d[1] for d in sorted_depts]
        
        bars = axes[0,2].bar(range(len(dept_names)), dept_rates, color='orange', alpha=0.7)
        axes[0,2].set_title('Turnover per Dipartimento (Top 6)')
        axes[0,2].set_ylabel('Turnover (%)')
        axes[0,2].set_xticks(range(len(dept_names)))
        axes[0,2].set_xticklabels(dept_names, rotation=45, ha='right')
    
    # Grafico 4: Distribuzione età attivi vs usciti
    if 'Eta' in df.columns:
        df_attivi = df[df['EmploymentStatus'] == 'Active']
        df_usciti = df[df['EmploymentStatus'] == 'Terminated']
        
        axes[1,0].hist(df_attivi['Eta'].dropna(), alpha=0.7, label='Attivi', bins=15, color='blue')
        axes[1,0].hist(df_usciti['Eta'].dropna(), alpha=0.7, label='Usciti', bins=15, color='red')
        axes[1,0].set_title('Distribuzione Età: Attivi vs Usciti')
        axes[1,0].set_xlabel('Età')
        axes[1,0].set_ylabel('Numero Dipendenti')
        axes[1,0].legend()
    
    # Grafico 5: Stipendio attivi vs usciti
    if 'Salary' in df.columns:
        df_attivi = df[df['EmploymentStatus'] == 'Active']
        df_usciti = df[df['EmploymentStatus'] == 'Terminated']
        
        box_data = [df_attivi['Salary'].dropna(), df_usciti['Salary'].dropna()]
        axes[1,1].boxplot(box_data, labels=['Attivi', 'Usciti'])
        axes[1,1].set_title('Distribuzione Stipendi: Attivi vs Usciti')
        axes[1,1].set_ylabel('Stipendio (€)')
    
    # Grafico 6: Heatmap turnover per dipartimento e genere
    if 'Department' in df.columns and 'Gender' in df.columns:
        # Crea matrice turnover
        depts = df['Department'].unique()[:6]  # Top 6 dipartimenti
        genders = ['M', 'F']
        
        turnover_matrix = []
        for dept in depts:
            dept_row = []
            for gender in genders:
                subset = df[(df['Department'] == dept) & (df['Gender'] == gender)]
                if len(subset) > 0:
                    usciti = len(subset[subset['EmploymentStatus'] == 'Terminated'])
                    turnover_rate = usciti / len(subset) * 100
                else:
                    turnover_rate = 0
                dept_row.append(turnover_rate)
            turnover_matrix.append(dept_row)
        
        import seaborn as sns
        sns.heatmap(turnover_matrix, annot=True, fmt='.1f', 
                   xticklabels=['Uomini', 'Donne'], yticklabels=depts,
                   cmap='Reds', ax=axes[1,2])
        axes[1,2].set_title('Turnover % per Dipartimento e Genere')
    
    plt.tight_layout()
    plt.show()
"""))
    
    # Sezione 4: Raccomandazioni
    notebook["cells"].append(crea_cella_markdown("""
## 🎯 Raccomandazioni Strategiche

Azioni concrete per migliorare la retention aziendale.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 🎯 RACCOMANDAZIONI STRATEGICHE TURNOVER
if df is not None and 'EmploymentStatus' in df.columns:
    
    print("🎯 RACCOMANDAZIONI STRATEGICHE PER RIDURRE IL TURNOVER")
    print("=" * 60)
    
    df_usciti = df[df['EmploymentStatus'] == 'Terminated']
    total_employees = len(df)
    turnover_globale = len(df_usciti) / total_employees * 100
    
    # Analisi gender gap
    if 'Gender' in df.columns:
        m_total = len(df[df['Gender'] == 'M'])
        f_total = len(df[df['Gender'] == 'F'])
        m_usciti = len(df_usciti[df_usciti['Gender'] == 'M'])
        f_usciti = len(df_usciti[df_usciti['Gender'] == 'F'])
        
        if m_total > 0 and f_total > 0:
            turnover_m = m_usciti / m_total * 100
            turnover_f = f_usciti / f_total * 100
            gap = turnover_f - turnover_m
            
            print(f"📊 **SITUAZIONE ATTUALE:**")
            print(f"   • Turnover globale: {turnover_globale:.1f}%")
            print(f"   • Turnover uomini: {turnover_m:.1f}%")
            print(f"   • Turnover donne: {turnover_f:.1f}%")
            print(f"   • Gender gap: {gap:.1f} punti percentuali")
            
            print(f"\\n🚨 **PRIORITÀ IMMEDIATE:**")
            
            if gap > 30:
                print(f"   1. 🆘 **EMERGENZA RETENTION FEMMINILE**")
                print(f"      → Exit interview immediate per tutte le donne uscite")
                print(f"      → Task force dedicata alla retention femminile")
                print(f"      → Revisione completa politiche HR")
                
            if gap > 20:
                print(f"   2. ⚖️  **ANALISI PAY EQUITY URGENTE**")
                print(f"      → Audit completo delle retribuzioni per genere")
                print(f"      → Correzione immediate dei gap salariali")
                print(f"      → Trasparenza retributiva")
                
            if turnover_f > 40:
                print(f"   3. 🏢 **REVISIONE CULTURA AZIENDALE**")
                print(f"      → Survey anonima su inclusività e appartenenza")
                print(f"      → Programmi di mentoring per donne")
                print(f"      → Leadership training su diversity & inclusion")
                
            print(f"\\n📋 **AZIONI A MEDIO TERMINE:**")
            print(f"   • 👥 Programmi di career development specifici per donne")
            print(f"   • 🏠 Politiche work-life balance più flessibili")
            print(f"   • 📈 Target di promozione femminile")
            print(f"   • 🎯 KPI retention per manager")
            print(f"   • 💬 Feedback continuo e stay interview")
            
            print(f"\\n📊 **MONITORAGGIO CONTINUO:**")
            print(f"   • Dashboard turnover in tempo reale")
            print(f"   • Report mensili per leadership")
            print(f"   • Alert automatici per trend negativi")
            print(f"   • Benchmark con industry standard")
    
    print(f"\\n💡 **NOTA**: Queste raccomandazioni sono generate automaticamente")
    print(f"    basandosi sui dati attuali. Personalizzare secondo il contesto aziendale.")
"""))
    
    # Salva il notebook aggiornato
    with open('03_Analisi_Turnover.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print("✅ Modulo Analisi Turnover popolato con successo!")

if __name__ == "__main__":
    popola_modulo_turnover()
