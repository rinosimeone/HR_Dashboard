import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

def genera_dataset_hr_realistico():
    """Genera un dataset HR realistico con le caratteristiche richieste."""
    
    print("🏭 Generazione Dataset HR Realistico per Azienda Italiana")
    print("=" * 60)
    
    # Parametri del dataset
    n_dipendenti = 200  # Dataset più piccolo ma significativo
    
    # Seed per riproducibilità
    np.random.seed(42)
    random.seed(42)
    
    # 1. MAGGIORANZA MASCHILE (70% uomini, 30% donne)
    genders = ['M'] * 140 + ['F'] * 60
    random.shuffle(genders)
    
    # 2. DISTRIBUZIONE ETÀ CON MOLTI PROSSIMI ALLA PENSIONE
    # Leggi italiane: pensione a 67 anni (o 42 anni di contributi)
    eta_distribution = []
    
    # 15% giovani (25-35 anni)
    eta_distribution.extend(np.random.randint(25, 36, 30))
    
    # 25% adulti (36-50 anni)  
    eta_distribution.extend(np.random.randint(36, 51, 50))
    
    # 35% maturi (51-60 anni)
    eta_distribution.extend(np.random.randint(51, 61, 70))
    
    # 25% prossimi pensione (61-67 anni) - MOLTI!
    eta_distribution.extend(np.random.randint(61, 68, 50))
    
    random.shuffle(eta_distribution)
    
    # Calcola date di nascita
    oggi = datetime.now()
    date_nascita = []
    for eta in eta_distribution:
        anno_nascita = oggi.year - eta
        mese = random.randint(1, 12)
        giorno = random.randint(1, 28)
        date_nascita.append(f"{mese:02d}/{giorno:02d}/{anno_nascita}")
    
    # 3. ANZIANITÀ CORRELATA CON STIPENDIO
    # Più anzianità = stipendio più alto (con variazioni)
    anzianita_anni = []
    stipendi = []
    
    for i, eta in enumerate(eta_distribution):
        # Anzianità basata sull'età (con variazioni realistiche)
        if eta < 30:
            anzianita = random.randint(1, 5)
        elif eta < 40:
            anzianita = random.randint(3, 15)
        elif eta < 50:
            anzianita = random.randint(8, 25)
        elif eta < 60:
            anzianita = random.randint(15, 35)
        else:  # Over 60
            anzianita = random.randint(25, 42)
        
        anzianita_anni.append(anzianita)
        
        # Calcola data assunzione
        anno_assunzione = oggi.year - anzianita
        mese = random.randint(1, 12)
        giorno = random.randint(1, 28)
        data_assunzione = f"{mese:02d}/{giorno:02d}/{anno_assunzione}"
        
        # STIPENDIO CORRELATO CON ANZIANITÀ + GENDER GAP
        base_salary = 25000 + (anzianita * 800)  # Base: 800€ per anno di anzianità
        
        # Variazione per ruolo
        ruolo_bonus = random.randint(-3000, 8000)
        stipendio_base = base_salary + ruolo_bonus
        
        # 4. GENDER PAY GAP EVIDENTE
        if genders[i] == 'F':
            # Donne guadagnano 15-25% in meno a parità di anzianità
            gender_penalty = random.uniform(0.75, 0.85)
            stipendio_finale = int(stipendio_base * gender_penalty)
        else:
            # Uomini: stipendio pieno + possibili bonus
            gender_bonus = random.uniform(1.0, 1.1)
            stipendio_finale = int(stipendio_base * gender_bonus)
        
        stipendi.append(max(stipendio_finale, 22000))  # Minimo legale
    
    # Genera altri campi
    nomi_maschili = ["Marco", "Giuseppe", "Antonio", "Francesco", "Alessandro", "Andrea", "Matteo", "Lorenzo", "Davide", "Simone", "Luca", "Stefano", "Federico", "Roberto", "Gabriele", "Riccardo", "Tommaso", "Edoardo", "Filippo", "Michele"]
    nomi_femminili = ["Giulia", "Sara", "Chiara", "Francesca", "Federica", "Valentina", "Paola", "Laura", "Martina", "Alessandra", "Silvia", "Roberta", "Claudia", "Monica", "Daniela", "Cristina", "Elena", "Simona", "Barbara", "Manuela"]
    
    cognomi = ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco", "Bruno", "Gallo", "Conti", "De Luca", "Mancini", "Costa", "Giordano", "Rizzo", "Lombardi", "Moretti"]
    
    # Genera nomi completi
    nomi_completi = []
    for i, gender in enumerate(genders):
        if gender == 'M':
            nome = random.choice(nomi_maschili)
        else:
            nome = random.choice(nomi_femminili)
        cognome = random.choice(cognomi)
        nomi_completi.append(f"{nome} {cognome}")
    
    # Dipartimenti tipici azienda italiana
    dipartimenti = ["Produzione", "Amministrazione", "Vendite", "IT", "Risorse Umane", "Qualità", "Logistica", "R&D", "Marketing", "Acquisti"]
    dept_list = []
    for _ in range(n_dipendenti):
        # Produzione ha più dipendenti (tipico azienda manifatturiera italiana)
        if random.random() < 0.4:
            dept_list.append("Produzione")
        else:
            dept_list.append(random.choice(dipartimenti[1:]))
    
    # Posizioni lavorative
    posizioni = ["Operaio", "Impiegato", "Quadro", "Dirigente", "Tecnico", "Specialista", "Coordinatore", "Responsabile", "Manager", "Analista"]
    
    # Stati civili
    stati_civili = ["Single", "Married", "Divorced", "Widowed"]
    
    # Performance scores
    performance_scores = ["Exceeds", "Fully Meets", "Partially Meets", "PIP", "Needs Improvement"]
    
    # Recruitment sources
    recruitment_sources = ["Company Website", "LinkedIn", "Indeed", "Employee Referral", "Recruiter", "Career Fair", "University"]
    
    # Crea il DataFrame
    data = {
        'EmployeeID': range(1, n_dipendenti + 1),
        'EmployeeName': nomi_completi,
        'Salary': stipendi,
        'Position': [random.choice(posizioni) for _ in range(n_dipendenti)],
        'State': ['IT'] * n_dipendenti,  # Tutti in Italia
        'DateOfBirth': date_nascita,
        'Gender': genders,
        'MaritalStatus': [random.choice(stati_civili) for _ in range(n_dipendenti)],
        'HiringDate': [f"{random.randint(1,12):02d}/{random.randint(1,28):02d}/{oggi.year - anzianita_anni[i]}" for i in range(n_dipendenti)],
        'TerminationDate': [''] * n_dipendenti,  # Tutti attivi
        'EmploymentStatus': ['Active'] * n_dipendenti,
        'Department': dept_list,
        'RecruitmentSource': [random.choice(recruitment_sources) for _ in range(n_dipendenti)],
        'PerformanceScore': [random.choice(performance_scores) for _ in range(n_dipendenti)]
    }
    
    df = pd.DataFrame(data)
    
    # Salva il dataset
    df.to_csv('hr_data_realistico.csv', index=False)
    
    # Statistiche del dataset generato
    print("✅ Dataset generato con successo!")
    print(f"\n📊 **Statistiche Dataset:**")
    print(f"   • Totale dipendenti: {len(df)}")
    print(f"   • Uomini: {len(df[df['Gender'] == 'M'])} ({len(df[df['Gender'] == 'M'])/len(df)*100:.1f}%)")
    print(f"   • Donne: {len(df[df['Gender'] == 'F'])} ({len(df[df['Gender'] == 'F'])/len(df)*100:.1f}%)")
    
    # Analisi età per pensioni
    df['DateOfBirth'] = pd.to_datetime(df['DateOfBirth'], format='%m/%d/%Y')
    df['Eta'] = (pd.Timestamp.now() - df['DateOfBirth']).dt.days / 365.25
    
    pensione_5_anni = len(df[df['Eta'] >= 62])  # Pensione tra 5 anni
    pensione_10_anni = len(df[df['Eta'] >= 57])  # Pensione tra 10 anni
    
    print(f"\n🏖️ **Proiezioni Pensionamento (Leggi Italiane):**")
    print(f"   • Pensione entro 5 anni (età ≥62): {pensione_5_anni} dipendenti ({pensione_5_anni/len(df)*100:.1f}%)")
    print(f"   • Pensione entro 10 anni (età ≥57): {pensione_10_anni} dipendenti ({pensione_10_anni/len(df)*100:.1f}%)")
    
    # Analisi correlazione anzianità-stipendio
    df['HiringDate'] = pd.to_datetime(df['HiringDate'], format='%m/%d/%Y')
    df['AnniServizio'] = (pd.Timestamp.now() - df['HiringDate']).dt.days / 365.25
    
    correlazione = df['AnniServizio'].corr(df['Salary'])
    print(f"\n💰 **Correlazione Anzianità-Stipendio:** {correlazione:.3f}")
    
    # Analisi gender pay gap
    stipendio_medio_m = df[df['Gender'] == 'M']['Salary'].mean()
    stipendio_medio_f = df[df['Gender'] == 'F']['Salary'].mean()
    gap_percentuale = (1 - stipendio_medio_f/stipendio_medio_m) * 100
    
    print(f"\n⚖️ **Gender Pay Gap:**")
    print(f"   • Stipendio medio uomini: €{stipendio_medio_m:,.0f}")
    print(f"   • Stipendio medio donne: €{stipendio_medio_f:,.0f}")
    print(f"   • Gap: {gap_percentuale:.1f}% (donne guadagnano meno)")
    
    print(f"\n💾 Dataset salvato come: hr_data_realistico.csv")
    
    return df

if __name__ == "__main__":
    df = genera_dataset_hr_realistico()
