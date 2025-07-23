"""
Script per completare rapidamente i moduli rimanenti.
"""

import json

def crea_cella_codice(codice):
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": codice.split('\n')
    }

def crea_cella_markdown(testo):
    return {
        "cell_type": "markdown", 
        "metadata": {},
        "source": testo.split('\n')
    }

def completa_modulo_retributiva():
    """Completa il modulo retributiva."""
    
    with open('02_Analisi_Retributiva.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    notebook["cells"] = notebook["cells"][:3]
    
    # Analisi Pay Gap
    notebook["cells"].append(crea_cella_markdown("""
## 💰 Analisi Gender Pay Gap

Analisi dettagliata delle differenze retributive per genere.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 💰 ANALISI GENDER PAY GAP
if df is not None and 'Salary' in df.columns:
    print("💰 ANALISI RETRIBUTIVA - GENDER PAY GAP")
    print("=" * 45)
    
    df_analisi = df[df['EmploymentStatus'] == 'Active'] if 'EmploymentStatus' in df.columns else df
    
    if 'Gender' in df_analisi.columns:
        # Statistiche per genere
        salary_by_gender = df_analisi.groupby('Gender')['Salary'].agg(['mean', 'median', 'std', 'count'])
        
        print("📊 **STATISTICHE RETRIBUTIVE PER GENERE:**")
        for gender in ['M', 'F']:
            if gender in salary_by_gender.index:
                stats = salary_by_gender.loc[gender]
                gender_label = "🚹 Uomini" if gender == 'M' else "🚺 Donne"
                print(f"\\n   {gender_label}:")
                print(f"      • Media: €{stats['mean']:,.0f}")
                print(f"      • Mediana: €{stats['median']:,.0f}")
                print(f"      • Dipendenti: {stats['count']:,}")
        
        # Calcola gender pay gap
        if 'M' in salary_by_gender.index and 'F' in salary_by_gender.index:
            salary_m = salary_by_gender.loc['M', 'mean']
            salary_f = salary_by_gender.loc['F', 'mean']
            gap_abs = salary_m - salary_f
            gap_pct = (gap_abs / salary_m) * 100
            
            print(f"\\n⚖️  **GENDER PAY GAP:**")
            print(f"   • Gap assoluto: €{gap_abs:,.0f}")
            print(f"   • Gap percentuale: {gap_pct:.1f}%")
            
            if gap_pct > 20:
                print(f"   🚨 **GAP CRITICO**: Differenza superiore al 20%")
                print(f"      → Audit retributivo URGENTE necessario")
            elif gap_pct > 10:
                print(f"   ⚠️  **GAP SIGNIFICATIVO**: Azione correttiva necessaria")
            elif gap_pct > 5:
                print(f"   📋 **GAP MODERATO**: Monitoraggio continuo")
            else:
                print(f"   ✅ **GAP CONTENUTO**: Situazione accettabile")
        
        # Analisi per dipartimento
        if 'Department' in df_analisi.columns:
            print(f"\\n🏢 **PAY GAP PER DIPARTIMENTO:**")
            
            for dept in df_analisi['Department'].unique():
                dept_df = df_analisi[df_analisi['Department'] == dept]
                if len(dept_df) > 5:  # Solo dipartimenti con almeno 5 dipendenti
                    dept_gender = dept_df.groupby('Gender')['Salary'].mean()
                    if 'M' in dept_gender.index and 'F' in dept_gender.index:
                        dept_gap = (dept_gender['M'] - dept_gender['F']) / dept_gender['M'] * 100
                        gap_icon = "🚨" if dept_gap > 25 else "⚠️" if dept_gap > 15 else "📊" if dept_gap > 5 else "✅"
                        print(f"   {gap_icon} {dept}: {dept_gap:.1f}% gap")
"""))
    
    # Correlazione Anzianità-Stipendio
    notebook["cells"].append(crea_cella_markdown("""
## 📈 Correlazione Anzianità-Stipendio

Analisi della relazione tra esperienza e retribuzione.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 📈 CORRELAZIONE ANZIANITÀ-STIPENDIO
if df is not None and 'Salary' in df.columns and 'AnniServizio' in df.columns:
    
    print("📈 ANALISI CORRELAZIONE ANZIANITÀ-STIPENDIO")
    print("=" * 50)
    
    df_analisi = df[df['EmploymentStatus'] == 'Active'] if 'EmploymentStatus' in df.columns else df
    
    # Calcola correlazione
    correlazione = df_analisi['AnniServizio'].corr(df_analisi['Salary'])
    
    print(f"📊 **CORRELAZIONE ANZIANITÀ-STIPENDIO:**")
    print(f"   • Coefficiente di correlazione: {correlazione:.3f}")
    
    if correlazione > 0.7:
        print(f"   ✅ **CORRELAZIONE FORTE**: Ottima progressione retributiva")
    elif correlazione > 0.5:
        print(f"   📊 **CORRELAZIONE MODERATA**: Buona progressione")
    elif correlazione > 0.3:
        print(f"   ⚠️  **CORRELAZIONE DEBOLE**: Rivedere politiche di avanzamento")
    else:
        print(f"   🚨 **CORRELAZIONE MOLTO DEBOLE**: Sistema retributivo da rivedere")
    
    # Analisi per fasce di anzianità
    fasce_anzianita = {
        'Nuovi (0-5 anni)': df_analisi[df_analisi['AnniServizio'] <= 5]['Salary'].mean(),
        'Junior (6-10 anni)': df_analisi[(df_analisi['AnniServizio'] > 5) & (df_analisi['AnniServizio'] <= 10)]['Salary'].mean(),
        'Senior (11-20 anni)': df_analisi[(df_analisi['AnniServizio'] > 10) & (df_analisi['AnniServizio'] <= 20)]['Salary'].mean(),
        'Veterani (> 20 anni)': df_analisi[df_analisi['AnniServizio'] > 20]['Salary'].mean()
    }
    
    print(f"\\n💰 **STIPENDIO MEDIO PER ANZIANITÀ:**")
    for fascia, stipendio in fasce_anzianita.items():
        if not pd.isna(stipendio):
            print(f"   • {fascia}: €{stipendio:,.0f}")
    
    # Visualizzazione scatter plot
    plt.figure(figsize=(12, 8))
    
    plt.subplot(2, 2, 1)
    plt.scatter(df_analisi['AnniServizio'], df_analisi['Salary'], alpha=0.6)
    plt.xlabel('Anni di Servizio')
    plt.ylabel('Stipendio (€)')
    plt.title(f'Correlazione Anzianità-Stipendio (r={correlazione:.3f})')
    
    # Linea di tendenza
    z = np.polyfit(df_analisi['AnniServizio'], df_analisi['Salary'], 1)
    p = np.poly1d(z)
    plt.plot(df_analisi['AnniServizio'], p(df_analisi['AnniServizio']), "r--", alpha=0.8)
    
    # Distribuzione stipendi
    plt.subplot(2, 2, 2)
    df_analisi['Salary'].hist(bins=20, alpha=0.7, color='lightgreen')
    plt.xlabel('Stipendio (€)')
    plt.ylabel('Frequenza')
    plt.title('Distribuzione Stipendi')
    
    # Boxplot per genere
    if 'Gender' in df_analisi.columns:
        plt.subplot(2, 2, 3)
        gender_data = [df_analisi[df_analisi['Gender'] == 'M']['Salary'].dropna(),
                      df_analisi[df_analisi['Gender'] == 'F']['Salary'].dropna()]
        plt.boxplot(gender_data, labels=['Uomini', 'Donne'])
        plt.ylabel('Stipendio (€)')
        plt.title('Distribuzione Stipendi per Genere')
    
    # Top dipartimenti per stipendio
    if 'Department' in df_analisi.columns:
        plt.subplot(2, 2, 4)
        dept_salary = df_analisi.groupby('Department')['Salary'].mean().sort_values(ascending=False).head(6)
        dept_salary.plot(kind='bar', color='orange', alpha=0.7)
        plt.ylabel('Stipendio Medio (€)')
        plt.title('Stipendio Medio per Dipartimento')
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
"""))
    
    with open('02_Analisi_Retributiva.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print("✅ Modulo Retributiva completato!")

def completa_modulo_performance():
    """Completa il modulo performance."""
    
    with open('05_Performance_Analysis.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    notebook["cells"] = notebook["cells"][:3]
    
    # Analisi Performance
    notebook["cells"].append(crea_cella_markdown("""
## 📈 Analisi Performance Scores

Distribuzione e analisi dei punteggi di performance.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 📈 ANALISI PERFORMANCE SCORES
if df is not None and 'PerformanceScore' in df.columns:
    print("📈 ANALISI PERFORMANCE E TALENTI")
    print("=" * 40)
    
    df_analisi = df[df['EmploymentStatus'] == 'Active'] if 'EmploymentStatus' in df.columns else df
    
    # Distribuzione performance
    perf_counts = df_analisi['PerformanceScore'].value_counts()
    total_employees = len(df_analisi)
    
    print("📊 **DISTRIBUZIONE PERFORMANCE SCORES:**")
    for score, count in perf_counts.items():
        pct = count / total_employees * 100
        score_icon = "🌟" if "Exceeds" in score else "✅" if "Fully" in score else "⚠️" if "Partially" in score else "🚨"
        print(f"   {score_icon} {score}: {count:,} dipendenti ({pct:.1f}%)")
    
    # Identifica top performer e low performer
    top_performers = perf_counts.get('Exceeds', 0)
    low_performers = perf_counts.get('PIP', 0) + perf_counts.get('Needs Improvement', 0)
    
    print(f"\\n🎯 **ANALISI TALENTI:**")
    print(f"   • 🌟 Top Performers: {top_performers} ({top_performers/total_employees*100:.1f}%)")
    print(f"   • 🚨 Low Performers: {low_performers} ({low_performers/total_employees*100:.1f}%)")
    
    if top_performers / total_employees < 0.1:
        print(f"   📈 **AZIONE**: Pochi top performer, sviluppare programmi di eccellenza")
    
    if low_performers / total_employees > 0.15:
        print(f"   📋 **AZIONE**: Molti low performer, rivedere training e supporto")
    
    # Performance per genere
    if 'Gender' in df_analisi.columns:
        print(f"\\n⚖️  **PERFORMANCE PER GENERE:**")
        
        for gender in ['M', 'F']:
            gender_label = "🚹 Uomini" if gender == 'M' else "🚺 Donne"
            gender_df = df_analisi[df_analisi['Gender'] == gender]
            
            if len(gender_df) > 0:
                gender_perf = gender_df['PerformanceScore'].value_counts()
                top_perf_gender = gender_perf.get('Exceeds', 0)
                pct_top = top_perf_gender / len(gender_df) * 100
                
                print(f"   {gender_label}: {top_perf_gender} top performers ({pct_top:.1f}%)")
    
    # Performance per dipartimento
    if 'Department' in df_analisi.columns:
        print(f"\\n🏢 **TOP PERFORMERS PER DIPARTIMENTO:**")
        
        for dept in df_analisi['Department'].unique():
            dept_df = df_analisi[df_analisi['Department'] == dept]
            if len(dept_df) > 0:
                dept_top = len(dept_df[dept_df['PerformanceScore'] == 'Exceeds'])
                pct_dept_top = dept_top / len(dept_df) * 100
                
                if dept_top > 0:
                    print(f"   • {dept}: {dept_top} top performers ({pct_dept_top:.1f}%)")
    
    # Visualizzazioni
    plt.figure(figsize=(15, 10))
    
    # Grafico 1: Distribuzione performance
    plt.subplot(2, 3, 1)
    perf_counts.plot(kind='bar', color='lightblue', alpha=0.7)
    plt.title('Distribuzione Performance Scores')
    plt.ylabel('Numero Dipendenti')
    plt.xticks(rotation=45)
    
    # Grafico 2: Performance per genere
    if 'Gender' in df_analisi.columns:
        plt.subplot(2, 3, 2)
        perf_gender = df_analisi.groupby(['Gender', 'PerformanceScore']).size().unstack(fill_value=0)
        perf_gender.plot(kind='bar', stacked=True, ax=plt.gca())
        plt.title('Performance per Genere')
        plt.ylabel('Numero Dipendenti')
        plt.xticks(rotation=0)
        plt.legend(bbox_to_anchor=(1.05, 1), loc='upper left')
    
    # Grafico 3: Performance vs Stipendio
    if 'Salary' in df_analisi.columns:
        plt.subplot(2, 3, 3)
        perf_salary = df_analisi.groupby('PerformanceScore')['Salary'].mean()
        perf_salary.plot(kind='bar', color='gold', alpha=0.7)
        plt.title('Stipendio Medio per Performance')
        plt.ylabel('Stipendio (€)')
        plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.show()
"""))
    
    with open('05_Performance_Analysis.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print("✅ Modulo Performance completato!")

def completa_report_esecutivo():
    """Completa il report esecutivo."""
    
    with open('06_Report_Esecutivo.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    notebook["cells"] = notebook["cells"][:3]
    
    # KPI Dashboard
    notebook["cells"].append(crea_cella_markdown("""
## 🎯 KPI Dashboard Esecutivo

Sintesi dei principali indicatori HR per la leadership.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 🎯 KPI DASHBOARD ESECUTIVO
if df is not None:
    print("🎯 REPORT ESECUTIVO HR - KPI DASHBOARD")
    print("=" * 50)
    
    df_analisi = df[df['EmploymentStatus'] == 'Active'] if 'EmploymentStatus' in df.columns else df
    total_employees = len(df_analisi)
    
    print(f"👥 **FORZA LAVORO TOTALE**: {total_employees:,} dipendenti")
    
    # KPI 1: Gender Balance
    if 'Gender' in df_analisi.columns:
        gender_counts = df_analisi['Gender'].value_counts()
        male_pct = gender_counts.get('M', 0) / total_employees * 100
        female_pct = gender_counts.get('F', 0) / total_employees * 100
        
        print(f"\\n⚖️  **EQUILIBRIO DI GENERE:**")
        print(f"   • Uomini: {male_pct:.1f}% | Donne: {female_pct:.1f}%")
        
        balance_status = "✅ Equilibrato" if abs(male_pct - female_pct) <= 15 else "⚠️ Squilibrato"
        print(f"   • Status: {balance_status}")
    
    # KPI 2: Età Media
    if 'Eta' in df_analisi.columns:
        eta_media = df_analisi['Eta'].mean()
        print(f"\\n🎂 **ETÀ MEDIA FORZA LAVORO**: {eta_media:.1f} anni")
        
        # Rischio pensionamenti
        over_60 = len(df_analisi[df_analisi['Eta'] >= 60])
        risk_pct = over_60 / total_employees * 100
        print(f"   • Dipendenti over 60: {over_60} ({risk_pct:.1f}%)")
        
        risk_status = "🚨 Alto" if risk_pct > 15 else "⚠️ Moderato" if risk_pct > 10 else "✅ Basso"
        print(f"   • Rischio pensionamenti: {risk_status}")
    
    # KPI 3: Turnover (se disponibile)
    if 'EmploymentStatus' in df.columns:
        df_usciti = df[df['EmploymentStatus'] == 'Terminated']
        turnover_rate = len(df_usciti) / len(df) * 100
        
        print(f"\\n🔄 **TASSO TURNOVER**: {turnover_rate:.1f}%")
        
        turnover_status = "🚨 Critico" if turnover_rate > 25 else "⚠️ Alto" if turnover_rate > 15 else "✅ Normale"
        print(f"   • Status: {turnover_status}")
        
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
                
                print(f"   • Gap turnover M/F: {gap:.1f} punti percentuali")
    
    # KPI 4: Pay Gap
    if 'Salary' in df_analisi.columns and 'Gender' in df_analisi.columns:
        salary_by_gender = df_analisi.groupby('Gender')['Salary'].mean()
        if 'M' in salary_by_gender.index and 'F' in salary_by_gender.index:
            pay_gap = (salary_by_gender['M'] - salary_by_gender['F']) / salary_by_gender['M'] * 100
            
            print(f"\\n💰 **GENDER PAY GAP**: {pay_gap:.1f}%")
            
            gap_status = "🚨 Critico" if pay_gap > 20 else "⚠️ Significativo" if pay_gap > 10 else "✅ Accettabile"
            print(f"   • Status: {gap_status}")
    
    # KPI 5: Performance
    if 'PerformanceScore' in df_analisi.columns:
        top_performers = len(df_analisi[df_analisi['PerformanceScore'] == 'Exceeds'])
        top_pct = top_performers / total_employees * 100
        
        print(f"\\n🌟 **TOP PERFORMERS**: {top_performers} ({top_pct:.1f}%)")
        
        talent_status = "✅ Ottimo" if top_pct > 15 else "📊 Buono" if top_pct > 10 else "⚠️ Da migliorare"
        print(f"   • Status talenti: {talent_status}")
    
    print(f"\\n🎯 **RACCOMANDAZIONI PRIORITARIE:**")
    
    # Raccomandazioni automatiche basate sui KPI
    raccomandazioni = []
    
    if 'EmploymentStatus' in df.columns and turnover_rate > 20:
        raccomandazioni.append("🚨 URGENTE: Ridurre turnover con programmi retention")
    
    if 'Gender' in df_analisi.columns and abs(male_pct - female_pct) > 20:
        raccomandazioni.append("⚖️ Migliorare equilibrio di genere nel recruiting")
    
    if 'Salary' in df_analisi.columns and 'Gender' in df_analisi.columns and pay_gap > 15:
        raccomandazioni.append("💰 Audit retributivo per ridurre pay gap")
    
    if 'Eta' in df_analisi.columns and risk_pct > 15:
        raccomandazioni.append("🏖️ Piano successione per pensionamenti imminenti")
    
    if not raccomandazioni:
        raccomandazioni.append("✅ Situazione HR stabile, mantenere standard attuali")
    
    for i, rec in enumerate(raccomandazioni, 1):
        print(f"   {i}. {rec}")
    
    print(f"\\n📊 Report generato automaticamente - {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
"""))
    
    with open('06_Report_Esecutivo.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print("✅ Report Esecutivo completato!")

if __name__ == "__main__":
    print("🚀 Completamento moduli rimanenti...")
    completa_modulo_retributiva()
    completa_modulo_performance() 
    completa_report_esecutivo()
    print("🎉 TUTTI I MODULI COMPLETATI!")
