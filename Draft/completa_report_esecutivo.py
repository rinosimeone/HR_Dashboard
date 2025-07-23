"""
Completamento avanzato del Report Esecutivo per leadership.
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

def completa_report_esecutivo():
    """Completa il Report Esecutivo con dashboard enterprise-grade."""
    
    print("📋 Completamento Report Esecutivo Enterprise...")
    
    # Carica il notebook esistente
    with open('06_Report_Esecutivo.ipynb', 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    # Mantieni solo header, setup e import (prime 3 celle)
    notebook["cells"] = notebook["cells"][:3]
    
    # Sezione 1: Executive Dashboard Completo
    notebook["cells"].append(crea_cella_markdown("""
## 🎯 Executive Dashboard - KPI Scorecard

Dashboard completo con KPI principali e sistema di alert per la leadership.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 🎯 EXECUTIVE DASHBOARD - KPI SCORECARD
if df is not None:
    print("🎯 EXECUTIVE DASHBOARD - HR SCORECARD")
    print("=" * 50)
    
    df_analisi = df[df['EmploymentStatus'] == 'Active'] if 'EmploymentStatus' in df.columns else df
    total_employees = len(df_analisi)
    
    # Funzione per status icon
    def get_status_icon(value, thresholds, reverse=False):
        \"\"\"Restituisce icona status basata su soglie.\"\"\"
        if reverse:  # Per metriche dove valori bassi sono buoni (es. turnover)
            if value <= thresholds[0]:
                return "🟢"
            elif value <= thresholds[1]:
                return "🟡"
            else:
                return "🔴"
        else:  # Per metriche dove valori alti sono buoni
            if value >= thresholds[1]:
                return "🟢"
            elif value >= thresholds[0]:
                return "🟡"
            else:
                return "🔴"
    
    print(f"👥 **WORKFORCE OVERVIEW**: {total_employees:,} dipendenti attivi")
    print(f"📅 **Report Date**: {pd.Timestamp.now().strftime('%d/%m/%Y %H:%M')}")
    
    # KPI 1: WORKFORCE COMPOSITION
    print(f"\\n📊 **1. WORKFORCE COMPOSITION**")
    
    if 'Gender' in df_analisi.columns:
        gender_counts = df_analisi['Gender'].value_counts()
        male_pct = gender_counts.get('M', 0) / total_employees * 100
        female_pct = gender_counts.get('F', 0) / total_employees * 100
        gender_gap = abs(male_pct - female_pct)
        
        # Status basato su equilibrio (gap < 15% = verde, < 25% = giallo, >= 25% = rosso)
        gender_status = get_status_icon(gender_gap, [15, 25], reverse=True)
        
        print(f"   {gender_status} **Gender Balance**: {male_pct:.1f}% M / {female_pct:.1f}% F")
        print(f"      • Gap: {gender_gap:.1f} punti percentuali")
        
        if gender_gap >= 25:
            print(f"      🚨 **AZIONE RICHIESTA**: Squilibrio critico")
        elif gender_gap >= 15:
            print(f"      ⚠️ **MONITORAGGIO**: Squilibrio moderato")
        else:
            print(f"      ✅ **TARGET RAGGIUNTO**: Equilibrio accettabile")
    
    # KPI 2: AGE DEMOGRAPHICS
    if 'Eta' in df_analisi.columns:
        eta_media = df_analisi['Eta'].mean()
        over_55 = len(df_analisi[df_analisi['Eta'] >= 55])
        under_35 = len(df_analisi[df_analisi['Eta'] < 35])
        
        over_55_pct = over_55 / total_employees * 100
        under_35_pct = under_35 / total_employees * 100
        
        # Status basato su rischio pensionamenti (< 20% over 55 = verde)
        age_status = get_status_icon(over_55_pct, [15, 25], reverse=True)
        
        print(f"\\n🎂 **2. AGE DEMOGRAPHICS**")
        print(f"   {age_status} **Age Profile**: Media {eta_media:.1f} anni")
        print(f"      • Over 55: {over_55} ({over_55_pct:.1f}%) - Rischio pensionamenti")
        print(f"      • Under 35: {under_35} ({under_35_pct:.1f}%) - Giovani talenti")
        
        if over_55_pct >= 25:
            print(f"      🚨 **ALTO RISCHIO**: Molti prossimi alla pensione")
        elif over_55_pct >= 15:
            print(f"      ⚠️ **MONITORAGGIO**: Pianificare sostituzioni")
        else:
            print(f"      ✅ **SITUAZIONE STABILE**: Rischio pensionamenti contenuto")
    
    # KPI 3: TURNOVER ANALYSIS
    if 'EmploymentStatus' in df.columns:
        df_usciti = df[df['EmploymentStatus'] == 'Terminated']
        turnover_rate = len(df_usciti) / len(df) * 100
        
        # Status turnover (< 15% = verde, < 25% = giallo, >= 25% = rosso)
        turnover_status = get_status_icon(turnover_rate, [15, 25], reverse=True)
        
        print(f"\\n🔄 **3. TURNOVER ANALYSIS**")
        print(f"   {turnover_status} **Overall Turnover**: {turnover_rate:.1f}%")
        
        # Gender gap turnover
        if 'Gender' in df.columns:
            m_total = len(df[df['Gender'] == 'M'])
            f_total = len(df[df['Gender'] == 'F'])
            m_usciti = len(df_usciti[df_usciti['Gender'] == 'M'])
            f_usciti = len(df_usciti[df_usciti['Gender'] == 'F'])
            
            if m_total > 0 and f_total > 0:
                turnover_m = m_usciti / m_total * 100
                turnover_f = f_usciti / f_total * 100
                turnover_gap = turnover_f - turnover_m
                
                gap_status = get_status_icon(abs(turnover_gap), [10, 20], reverse=True)
                
                print(f"   {gap_status} **Gender Gap**: {turnover_gap:.1f} punti (M: {turnover_m:.1f}% / F: {turnover_f:.1f}%)")
                
                if abs(turnover_gap) >= 20:
                    print(f"      🚨 **EMERGENZA**: Gap critico - azione immediata")
                elif abs(turnover_gap) >= 10:
                    print(f"      ⚠️ **ATTENZIONE**: Gap significativo")
                else:
                    print(f"      ✅ **EQUILIBRATO**: Gap contenuto")
    
    # KPI 4: COMPENSATION EQUITY
    if 'Salary' in df_analisi.columns and 'Gender' in df_analisi.columns:
        salary_by_gender = df_analisi.groupby('Gender')['Salary'].mean()
        
        if 'M' in salary_by_gender.index and 'F' in salary_by_gender.index:
            pay_gap = (salary_by_gender['M'] - salary_by_gender['F']) / salary_by_gender['M'] * 100
            
            # Status pay gap (< 5% = verde, < 15% = giallo, >= 15% = rosso)
            pay_status = get_status_icon(pay_gap, [5, 15], reverse=True)
            
            print(f"\\n💰 **4. COMPENSATION EQUITY**")
            print(f"   {pay_status} **Gender Pay Gap**: {pay_gap:.1f}%")
            print(f"      • Stipendio medio M: €{salary_by_gender['M']:,.0f}")
            print(f"      • Stipendio medio F: €{salary_by_gender['F']:,.0f}")
            
            if pay_gap >= 15:
                print(f"      🚨 **AUDIT URGENTE**: Gap critico")
            elif pay_gap >= 5:
                print(f"      ⚠️ **REVISIONE**: Gap da monitorare")
            else:
                print(f"      ✅ **EQUITÀ**: Gap accettabile")
    
    # KPI 5: PERFORMANCE HEALTH
    if 'PerformanceScore' in df_analisi.columns:
        top_performers = len(df_analisi[df_analisi['PerformanceScore'] == 'Exceeds'])
        low_performers = len(df_analisi[df_analisi['PerformanceScore'].isin(['PIP', 'Needs Improvement'])])
        
        top_pct = top_performers / total_employees * 100
        low_pct = low_performers / total_employees * 100
        
        # Status performance (> 15% top = verde, > 10% = giallo, <= 10% = rosso)
        perf_status = get_status_icon(top_pct, [10, 15])
        
        print(f"\\n📈 **5. PERFORMANCE HEALTH**")
        print(f"   {perf_status} **Top Performers**: {top_performers} ({top_pct:.1f}%)")
        print(f"   🔴 **Low Performers**: {low_performers} ({low_pct:.1f}%)")
        
        if top_pct <= 5:
            print(f"      🚨 **CARENZA TALENTI**: Pochi top performers")
        elif low_pct >= 15:
            print(f"      🚨 **PERFORMANCE RISK**: Molti low performers")
        elif top_pct >= 15:
            print(f"      ✅ **ECCELLENZA**: Buona distribuzione talenti")
        else:
            print(f"      📊 **STANDARD**: Performance nella norma")
"""))
    
    # Sezione 2: Risk Assessment Matrix
    notebook["cells"].append(crea_cella_markdown("""
## 🚨 Risk Assessment Matrix

Matrice di rischio HR con early warning system per la leadership.
"""))
    
    notebook["cells"].append(crea_cella_codice("""
# 🚨 RISK ASSESSMENT MATRIX
if df is not None:
    
    print("🚨 HR RISK ASSESSMENT MATRIX")
    print("=" * 35)
    
    # Calcola risk scores per ogni area
    risk_scores = {}
    risk_details = {}
    
    # Risk 1: Turnover Risk
    if 'EmploymentStatus' in df.columns:
        turnover_rate = len(df[df['EmploymentStatus'] == 'Terminated']) / len(df) * 100
        
        if turnover_rate >= 30:
            risk_scores['Turnover'] = 'HIGH'
            risk_details['Turnover'] = f"Turnover critico: {turnover_rate:.1f}%"
        elif turnover_rate >= 20:
            risk_scores['Turnover'] = 'MEDIUM'
            risk_details['Turnover'] = f"Turnover elevato: {turnover_rate:.1f}%"
        else:
            risk_scores['Turnover'] = 'LOW'
            risk_details['Turnover'] = f"Turnover normale: {turnover_rate:.1f}%"
    
    # Risk 2: Succession Risk (pensionamenti)
    if 'Eta' in df_analisi.columns:
        near_retirement = len(df_analisi[df_analisi['Eta'] >= 60])
        retirement_risk_pct = near_retirement / len(df_analisi) * 100
        
        if retirement_risk_pct >= 20:
            risk_scores['Succession'] = 'HIGH'
            risk_details['Succession'] = f"Molti prossimi pensione: {retirement_risk_pct:.1f}%"
        elif retirement_risk_pct >= 10:
            risk_scores['Succession'] = 'MEDIUM'
            risk_details['Succession'] = f"Rischio pensionamenti: {retirement_risk_pct:.1f}%"
        else:
            risk_scores['Succession'] = 'LOW'
            risk_details['Succession'] = f"Rischio pensionamenti basso: {retirement_risk_pct:.1f}%"
    
    # Risk 3: Talent Risk
    if 'PerformanceScore' in df_analisi.columns:
        top_performers = len(df_analisi[df_analisi['PerformanceScore'] == 'Exceeds'])
        top_pct = top_performers / len(df_analisi) * 100
        
        if top_pct <= 5:
            risk_scores['Talent'] = 'HIGH'
            risk_details['Talent'] = f"Carenza top performers: {top_pct:.1f}%"
        elif top_pct <= 10:
            risk_scores['Talent'] = 'MEDIUM'
            risk_details['Talent'] = f"Pochi top performers: {top_pct:.1f}%"
        else:
            risk_scores['Talent'] = 'LOW'
            risk_details['Talent'] = f"Buoni top performers: {top_pct:.1f}%"
    
    # Risk 4: Equity Risk (pay gap)
    if 'Salary' in df_analisi.columns and 'Gender' in df_analisi.columns:
        salary_by_gender = df_analisi.groupby('Gender')['Salary'].mean()
        
        if 'M' in salary_by_gender.index and 'F' in salary_by_gender.index:
            pay_gap = (salary_by_gender['M'] - salary_by_gender['F']) / salary_by_gender['M'] * 100
            
            if pay_gap >= 20:
                risk_scores['Equity'] = 'HIGH'
                risk_details['Equity'] = f"Pay gap critico: {pay_gap:.1f}%"
            elif pay_gap >= 10:
                risk_scores['Equity'] = 'MEDIUM'
                risk_details['Equity'] = f"Pay gap significativo: {pay_gap:.1f}%"
            else:
                risk_scores['Equity'] = 'LOW'
                risk_details['Equity'] = f"Pay gap accettabile: {pay_gap:.1f}%"
    
    # Risk 5: Diversity Risk
    if 'Gender' in df_analisi.columns:
        gender_counts = df_analisi['Gender'].value_counts()
        male_pct = gender_counts.get('M', 0) / len(df_analisi) * 100
        female_pct = gender_counts.get('F', 0) / len(df_analisi) * 100
        gender_gap = abs(male_pct - female_pct)
        
        if gender_gap >= 40:
            risk_scores['Diversity'] = 'HIGH'
            risk_details['Diversity'] = f"Squilibrio estremo: {gender_gap:.1f}% gap"
        elif gender_gap >= 25:
            risk_scores['Diversity'] = 'MEDIUM'
            risk_details['Diversity'] = f"Squilibrio significativo: {gender_gap:.1f}% gap"
        else:
            risk_scores['Diversity'] = 'LOW'
            risk_details['Diversity'] = f"Equilibrio accettabile: {gender_gap:.1f}% gap"
    
    # Visualizza Risk Matrix
    print("🎯 **RISK MATRIX SUMMARY:**")
    print()
    
    risk_icons = {
        'HIGH': '🔴',
        'MEDIUM': '🟡', 
        'LOW': '🟢'
    }
    
    high_risks = []
    medium_risks = []
    
    for risk_area, risk_level in risk_scores.items():
        icon = risk_icons.get(risk_level, '⚪')
        detail = risk_details.get(risk_area, '')
        
        print(f"   {icon} **{risk_area.upper()} RISK**: {risk_level}")
        print(f"      └─ {detail}")
        
        if risk_level == 'HIGH':
            high_risks.append(risk_area)
        elif risk_level == 'MEDIUM':
            medium_risks.append(risk_area)
    
    # Overall Risk Assessment
    total_risks = len(risk_scores)
    high_count = len(high_risks)
    medium_count = len(medium_risks)
    
    print(f"\\n🎯 **OVERALL RISK ASSESSMENT:**")
    
    if high_count >= 3:
        overall_risk = "🔴 CRITICAL"
        print(f"   {overall_risk}: {high_count}/{total_risks} aree ad alto rischio")
        print(f"   🚨 **AZIONE IMMEDIATA RICHIESTA**")
    elif high_count >= 1 or medium_count >= 3:
        overall_risk = "🟡 ELEVATED"
        print(f"   {overall_risk}: {high_count} alto + {medium_count} medio rischio")
        print(f"   ⚠️ **MONITORAGGIO ATTIVO NECESSARIO**")
    else:
        overall_risk = "🟢 MANAGEABLE"
        print(f"   {overall_risk}: Rischi sotto controllo")
        print(f"   ✅ **SITUAZIONE STABILE**")
    
    # Early Warning Indicators
    print(f"\\n⚡ **EARLY WARNING INDICATORS:**")
    
    warnings = []
    
    # Check trend indicators (simulati)
    if 'EmploymentStatus' in df.columns:
        recent_exits = len(df[df['EmploymentStatus'] == 'Terminated'])
        if recent_exits > len(df) * 0.15:  # > 15% usciti
            warnings.append("📈 Trend turnover in aumento")
    
    if 'Eta' in df_analisi.columns:
        avg_age = df_analisi['Eta'].mean()
        if avg_age > 50:
            warnings.append("👴 Workforce aging rapidamente")
    
    if 'PerformanceScore' in df_analisi.columns:
        low_perf = len(df_analisi[df_analisi['PerformanceScore'].isin(['PIP', 'Needs Improvement'])])
        if low_perf > len(df_analisi) * 0.15:
            warnings.append("📉 Performance in declino")
    
    if warnings:
        for warning in warnings:
            print(f"   ⚠️ {warning}")
    else:
        print(f"   ✅ Nessun warning attivo")
    
    # Raccomandazioni immediate
    print(f"\\n🎯 **RACCOMANDAZIONI IMMEDIATE:**")
    
    if high_risks:
        print(f"   🚨 **PRIORITÀ ASSOLUTA** - Aree ad alto rischio:")
        for risk in high_risks:
            if risk == 'Turnover':
                print(f"      • {risk}: Exit interview, retention programs, cultura aziendale")
            elif risk == 'Succession':
                print(f"      • {risk}: Piano successione, knowledge transfer, hiring")
            elif risk == 'Talent':
                print(f"      • {risk}: Talent acquisition, development programs, retention")
            elif risk == 'Equity':
                print(f"      • {risk}: Pay audit, compensation review, policy revision")
            elif risk == 'Diversity':
                print(f"      • {risk}: Diversity recruiting, inclusion programs, bias training")
    
    if medium_risks:
        print(f"   📊 **MONITORAGGIO ATTIVO** - Aree a medio rischio:")
        for risk in medium_risks:
            print(f"      • {risk}: Monitoraggio mensile, azioni preventive")
    
    if not high_risks and not medium_risks:
        print(f"   ✅ **MANTENIMENTO**: Continuare strategie attuali")
"""))
    
    # Salva il notebook aggiornato
    with open('06_Report_Esecutivo.ipynb', 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print("✅ Report Esecutivo completato con Risk Assessment!")

if __name__ == "__main__":
    completa_report_esecutivo()
