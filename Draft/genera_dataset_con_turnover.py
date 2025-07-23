import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def genera_dataset_con_alto_turnover():
    """Genera un dataset HR con alto turnover, specialmente tra le donne."""
    
    print("🔄 Generazione Dataset HR con Alto Turnover Femminile")
    print("=" * 60)
    
    # Parametri del dataset
    n_dipendenti_totali = 300  # Dataset più grande per mostrare il turnover
    n_dipendenti_attivi = 200  # Dipendenti attualmente attivi
    n_dipendenti_usciti = 100  # Dipendenti che hanno lasciato l'azienda
    
    # Seed per riproducibilità
    np.random.seed(42)
    random.seed(42)
    
    # 1. MAGGIORANZA MASCHILE tra gli ATTIVI (70% uomini, 30% donne)
    # Ma tra chi ha lasciato l'azienda, 70% sono donne!
    
    # Dipendenti attivi: 70% uomini, 30% donne
    genders_attivi = ['M'] * 140 + ['F'] * 60
    
    # Dipendenti usciti: 30% uomini, 70% donne (ALTO TURNOVER FEMMINILE!)
    genders_usciti = ['M'] * 30 + ['F'] * 70
    
    # Combina tutti
    all_genders = genders_attivi + genders_usciti
    random.shuffle(all_genders)
    
    # Status: primi 200 attivi, ultimi 100 usciti
    employment_status = ['Active'] * n_dipendenti_attivi + ['Terminated'] * n_dipendenti_usciti
    
    print(f"📊 Composizione pianificata:")
    print(f"   • Dipendenti attivi: {n_dipendenti_attivi} (70% M, 30% F)")
    print(f"   • Dipendenti usciti: {n_dipendenti_usciti} (30% M, 70% F)")
    
    # 2. DISTRIBUZIONE ETÀ CON MOLTI PROSSIMI ALLA PENSIONE
    eta_distribution = []
    
    # Per dipendenti attivi
    for i in range(n_dipendenti_attivi):
        if i < 30:  # 15% giovani (25-35 anni)
            eta_distribution.append(np.random.randint(25, 36))
        elif i < 80:  # 25% adulti (36-50 anni)
            eta_distribution.append(np.random.randint(36, 51))
        elif i < 150:  # 35% maturi (51-60 anni)
            eta_distribution.append(np.random.randint(51, 61))
        else:  # 25% prossimi pensione (61-67 anni)
            eta_distribution.append(np.random.randint(61, 68))
    
    # Per dipendenti usciti (più giovani - tipico del turnover)
    for i in range(n_dipendenti_usciti):
        if i < 40:  # 40% giovani che se ne vanno
            eta_distribution.append(np.random.randint(25, 35))
        elif i < 70:  # 30% adulti
            eta_distribution.append(np.random.randint(35, 45))
        elif i < 90:  # 20% maturi
            eta_distribution.append(np.random.randint(45, 55))
        else:  # 10% senior
            eta_distribution.append(np.random.randint(55, 65))
    
    # Calcola date di nascita
    oggi = datetime.now()
    date_nascita = []
    for eta in eta_distribution:
        anno_nascita = oggi.year - eta
        mese = random.randint(1, 12)
        giorno = random.randint(1, 28)
        date_nascita.append(f"{mese:02d}/{giorno:02d}/{anno_nascita}")
    
    # 3. ANZIANITÀ E STIPENDI CON CORRELAZIONE + GENDER GAP
    anzianita_anni = []
    stipendi = []
    date_assunzione = []
    date_terminazione = []
    
    for i in range(n_dipendenti_totali):
        eta = eta_distribution[i]
        is_active = i < n_dipendenti_attivi
        gender = all_genders[i]
        
        # Anzianità basata sull'età e status
        if is_active:
            # Dipendenti attivi: anzianità normale
            if eta < 30:
                anzianita = random.randint(1, 5)
            elif eta < 40:
                anzianita = random.randint(3, 15)
            elif eta < 50:
                anzianita = random.randint(8, 25)
            elif eta < 60:
                anzianita = random.randint(15, 35)
            else:
                anzianita = random.randint(25, 42)
        else:
            # Dipendenti usciti: anzianità più bassa (se ne vanno prima)
            if gender == 'F':
                # Donne se ne vanno ancora prima!
                anzianita = random.randint(1, 8)  # Max 8 anni
            else:
                anzianita = random.randint(2, 12)  # Max 12 anni
        
        anzianita_anni.append(anzianita)
        
        # Data assunzione
        anno_assunzione = oggi.year - anzianita
        mese_assunzione = random.randint(1, 12)
        giorno_assunzione = random.randint(1, 28)
        data_assunzione.append(f"{mese_assunzione:02d}/{giorno_assunzione:02d}/{anno_assunzione}")
        
        # Data terminazione (solo per chi ha lasciato)
        if not is_active:
            # Terminazione negli ultimi 3 anni
            anni_fa_terminazione = random.uniform(0.1, 3.0)
            data_term = oggi - timedelta(days=int(anni_fa_terminazione * 365))
            date_terminazione.append(f"{data_term.month:02d}/{data_term.day:02d}/{data_term.year}")
        else:
            date_terminazione.append('')
        
        # STIPENDIO CORRELATO CON ANZIANITÀ + GENDER GAP ESTREMO
        base_salary = 25000 + (anzianita * 800)
        ruolo_bonus = random.randint(-3000, 8000)
        stipendio_base = base_salary + ruolo_bonus
        
        # GENDER PAY GAP MOLTO EVIDENTE
        if gender == 'F':
            # Donne guadagnano 20-30% in meno!
            gender_penalty = random.uniform(0.70, 0.80)
            stipendio_finale = int(stipendio_base * gender_penalty)
        else:
            # Uomini: stipendio pieno + bonus
            gender_bonus = random.uniform(1.0, 1.15)
            stipendio_finale = int(stipendio_base * gender_bonus)
        
        stipendi.append(max(stipendio_finale, 22000))
    
    # Genera altri campi
    nomi_maschili = ["Marco", "Giuseppe", "Antonio", "Francesco", "Alessandro", "Andrea", "Matteo", "Lorenzo", "Davide", "Simone", "Luca", "Stefano", "Federico", "Roberto", "Gabriele", "Riccardo", "Tommaso", "Edoardo", "Filippo", "Michele"]
    nomi_femminili = ["Giulia", "Sara", "Chiara", "Francesca", "Federica", "Valentina", "Paola", "Laura", "Martina", "Alessandra", "Silvia", "Roberta", "Claudia", "Monica", "Daniela", "Cristina", "Elena", "Simona", "Barbara", "Manuela"]
    cognomi = ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca", "Mancini", "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti"]
    
    # Genera nomi completi
    nomi_completi = []
    for i, gender in enumerate(all_genders):
        if gender == 'M':
            nome = random.choice(nomi_maschili)
        else:
            nome = random.choice(nomi_femminili)
        cognome = random.choice(cognomi)
        nomi_completi.append(f"{nome} {cognome}")
    
    # Dipartimenti con diverso turnover
    dipartimenti = ["Produzione", "Amministrazione", "Vendite", "IT", "Risorse Umane", "Qualità", "Logistica", "R&D", "Marketing", "Acquisti"]
    dept_list = []
    
    for i in range(n_dipendenti_totali):
        is_active = i < n_dipendenti_attivi
        gender = all_genders[i]
        
        # Dipartimenti con alto turnover femminile
        if not is_active and gender == 'F':
            # Donne lasciano più spesso Vendite, Marketing, Amministrazione
            high_turnover_depts = ["Vendite", "Marketing", "Amministrazione", "Risorse Umane"]
            dept_list.append(random.choice(high_turnover_depts))
        elif random.random() < 0.4:
            dept_list.append("Produzione")
        else:
            dept_list.append(random.choice(dipartimenti[1:]))
    
    # Altri campi
    posizioni = ["Operaio", "Impiegato", "Quadro", "Dirigente", "Tecnico", "Specialista", "Coordinatore", "Responsabile", "Manager", "Analista"]
    stati_civili = ["Single", "Married", "Divorced", "Widowed"]
    performance_scores = ["Exceeds", "Fully Meets", "Partially Meets", "PIP", "Needs Improvement"]
    recruitment_sources = ["Company Website", "LinkedIn", "Indeed", "Employee Referral", "Recruiter", "Career Fair", "University"]
    
    # Crea il DataFrame
    data = {
        'EmployeeID': range(1, n_dipendenti_totali + 1),
        'EmployeeName': nomi_completi,
        'Salary': stipendi,
        'Position': [random.choice(posizioni) for _ in range(n_dipendenti_totali)],
        'State': ['IT'] * n_dipendenti_totali,
        'DateOfBirth': date_nascita,
        'Gender': all_genders,
        'MaritalStatus': [random.choice(stati_civili) for _ in range(n_dipendenti_totali)],
        'HiringDate': date_assunzione,
        'TerminationDate': date_terminazione,
        'EmploymentStatus': employment_status,
        'Department': dept_list,
        'RecruitmentSource': [random.choice(recruitment_sources) for _ in range(n_dipendenti_totali)],
        'PerformanceScore': [random.choice(performance_scores) for _ in range(n_dipendenti_totali)]
    }
    
    df = pd.DataFrame(data)
    
    # Salva il dataset
    df.to_csv('hr_data_con_turnover.csv', index=False)
    
    # ANALISI DEL TURNOVER
    print("✅ Dataset generato con successo!")
    
    # Analisi dipendenti attivi
    df_attivi = df[df['EmploymentStatus'] == 'Active']
    print(f"\n📊 **DIPENDENTI ATTIVI:**")
    print(f"   • Totale: {len(df_attivi)}")
    print(f"   • Uomini: {len(df_attivi[df_attivi['Gender'] == 'M'])} ({len(df_attivi[df_attivi['Gender'] == 'M'])/len(df_attivi)*100:.1f}%)")
    print(f"   • Donne: {len(df_attivi[df_attivi['Gender'] == 'F'])} ({len(df_attivi[df_attivi['Gender'] == 'F'])/len(df_attivi)*100:.1f}%)")
    
    # Analisi dipendenti usciti
    df_usciti = df[df['EmploymentStatus'] == 'Terminated']
    print(f"\n📊 **DIPENDENTI USCITI (TURNOVER):**")
    print(f"   • Totale: {len(df_usciti)}")
    print(f"   • Uomini: {len(df_usciti[df_usciti['Gender'] == 'M'])} ({len(df_usciti[df_usciti['Gender'] == 'M'])/len(df_usciti)*100:.1f}%)")
    print(f"   • Donne: {len(df_usciti[df_usciti['Gender'] == 'F'])} ({len(df_usciti[df_usciti['Gender'] == 'F'])/len(df_usciti)*100:.1f}%)")
    
    # Calcolo tasso di turnover per genere
    # Assumiamo che negli ultimi 3 anni ci fossero più dipendenti
    dipendenti_iniziali_m = len(df_attivi[df_attivi['Gender'] == 'M']) + len(df_usciti[df_usciti['Gender'] == 'M'])
    dipendenti_iniziali_f = len(df_attivi[df_attivi['Gender'] == 'F']) + len(df_usciti[df_usciti['Gender'] == 'F'])
    
    turnover_rate_m = len(df_usciti[df_usciti['Gender'] == 'M']) / dipendenti_iniziali_m * 100
    turnover_rate_f = len(df_usciti[df_usciti['Gender'] == 'F']) / dipendenti_iniziali_f * 100
    
    print(f"\n🔄 **TASSO DI TURNOVER (ultimi 3 anni):**")
    print(f"   • Uomini: {turnover_rate_m:.1f}%")
    print(f"   • Donne: {turnover_rate_f:.1f}%")
    print(f"   • Differenza: {turnover_rate_f - turnover_rate_m:.1f} punti percentuali")
    
    # Analisi per dipartimento
    print(f"\n🏢 **TURNOVER PER DIPARTIMENTO:**")
    dept_turnover = df_usciti['Department'].value_counts()
    for dept, count in dept_turnover.head().items():
        total_dept = len(df[df['Department'] == dept])
        rate = count / total_dept * 100
        print(f"   • {dept}: {count}/{total_dept} usciti ({rate:.1f}%)")
    
    # Gender pay gap
    stipendio_medio_m = df_attivi[df_attivi['Gender'] == 'M']['Salary'].mean()
    stipendio_medio_f = df_attivi[df_attivi['Gender'] == 'F']['Salary'].mean()
    gap_percentuale = (stipendio_medio_m - stipendio_medio_f) / stipendio_medio_m * 100
    
    print(f"\n⚖️ **GENDER PAY GAP (dipendenti attivi):**")
    print(f"   • Stipendio medio uomini: €{stipendio_medio_m:,.0f}")
    print(f"   • Stipendio medio donne: €{stipendio_medio_f:,.0f}")
    print(f"   • Gap: {gap_percentuale:.1f}%")
    
    print(f"\n💾 Dataset salvato come: hr_data_con_turnover.csv")
    print(f"🚨 SITUAZIONE CRITICA: Alto turnover femminile rilevato!")
    
    return df

if __name__ == "__main__":
    df = genera_dataset_con_alto_turnover()
