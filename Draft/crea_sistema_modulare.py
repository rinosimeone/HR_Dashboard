"""
Script per creare un sistema modulare di notebook HR.
Divide l'analisi in moduli specializzati per migliore organizzazione.
"""

import os
import json
from datetime import datetime

def crea_notebook_vuoto(titolo, descrizione):
    """Crea la struttura base di un notebook Jupyter."""
    
    notebook = {
        "cells": [
            {
                "cell_type": "markdown",
                "metadata": {},
                "source": [
                    f"# {titolo}\n",
                    "\n",
                    f"{descrizione}\n",
                    "\n",
                    f"**Data creazione**: {datetime.now().strftime('%d/%m/%Y')}\n",
                    "\n",
                    "---"
                ]
            },
            {
                "cell_type": "code",
                "execution_count": None,
                "metadata": {},
                "outputs": [],
                "source": [
                    "# Setup iniziale\n",
                    "import pandas as pd\n",
                    "import numpy as np\n",
                    "import matplotlib.pyplot as plt\n",
                    "import seaborn as sns\n",
                    "from datetime import datetime, timedelta\n",
                    "import warnings\n",
                    "warnings.filterwarnings('ignore')\n",
                    "\n",
                    "# Configurazione grafici\n",
                    "plt.style.use('default')\n",
                    "sns.set_palette('viridis')\n",
                    "plt.rcParams['figure.figsize'] = (12, 8)\n",
                    "\n",
                    "print(f'📊 {titolo} - Setup completato!')"
                ]
            }
        ],
        "metadata": {
            "kernelspec": {
                "display_name": "Python 3",
                "language": "python",
                "name": "python3"
            },
            "language_info": {
                "name": "python",
                "version": "3.8.0"
            }
        },
        "nbformat": 4,
        "nbformat_minor": 4
    }
    
    return notebook

def crea_cella_codice(codice, descrizione=""):
    """Crea una cella di codice per il notebook."""
    
    cella = {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": codice.split('\n')
    }
    
    return cella

def crea_cella_markdown(testo):
    """Crea una cella markdown per il notebook."""
    
    cella = {
        "cell_type": "markdown",
        "metadata": {},
        "source": testo.split('\n')
    }
    
    return cella

def crea_notebook_dashboard():
    """Crea il notebook dashboard principale."""
    
    print("📊 Creazione Notebook Dashboard Principale...")
    
    notebook = crea_notebook_vuoto(
        "🎯 HR Analytics Dashboard - Panoramica Generale",
        "Dashboard principale per l'analisi HR con collegamenti ai moduli specializzati."
    )
    
    # Cella di caricamento dati
    cella_caricamento = crea_cella_codice("""
# 📁 CARICAMENTO DATI HR
def carica_dati_hr():
    \"\"\"Carica e prepara i dati HR per l'analisi.\"\"\"
    
    try:
        # Prova prima il dataset con turnover
        df = pd.read_csv('hr_data_con_turnover.csv')
        print(f"✅ Dataset con turnover caricato: {len(df)} dipendenti")
        dataset_type = "turnover"
    except FileNotFoundError:
        try:
            # Fallback al dataset originale
            df = pd.read_csv('hr_data.csv')
            print(f"✅ Dataset originale caricato: {len(df)} dipendenti")
            dataset_type = "originale"
        except FileNotFoundError:
            print("❌ Nessun dataset trovato!")
            return None, None
    
    # Converti le date
    date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp.now()
    if 'DateOfBirth' in df.columns:
        eta_days = (oggi - df['DateOfBirth']).dt.days
        df['Eta'] = (eta_days / 365.25).round().astype('Int64')
    
    if 'HiringDate' in df.columns:
        servizio_days = (oggi - df['HiringDate']).dt.days
        df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')
        df['AnnoAssunzione'] = df['HiringDate'].dt.year
    
    print(f"📊 Dati preparati per l'analisi!")
    return df, dataset_type

# Carica i dati
df, dataset_type = carica_dati_hr()
""")
    
    # Cella panoramica generale
    cella_panoramica = crea_cella_codice("""
# 📊 PANORAMICA GENERALE
if df is not None:
    print("🎯 DASHBOARD HR - PANORAMICA GENERALE")
    print("=" * 60)
    
    # Statistiche base
    total_employees = len(df)
    print(f"👥 **Totale Dipendenti**: {total_employees:,}")
    
    # Analisi per status (se presente)
    if 'EmploymentStatus' in df.columns:
        status_counts = df['EmploymentStatus'].value_counts()
        print(f"\\n📊 **Status Dipendenti**:")
        for status, count in status_counts.items():
            pct = count / total_employees * 100
            print(f"   • {status}: {count:,} ({pct:.1f}%)")
    
    # Analisi per genere
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        print(f"\\n👥 **Distribuzione Genere**:")
        for gender, count in gender_counts.items():
            pct = count / total_employees * 100
            gender_label = "Uomini" if gender == 'M' else "Donne"
            print(f"   • {gender_label}: {count:,} ({pct:.1f}%)")
    
    # Statistiche età
    if 'Eta' in df.columns:
        eta_stats = df['Eta'].describe()
        print(f"\\n🎂 **Statistiche Età**:")
        print(f"   • Media: {eta_stats['mean']:.1f} anni")
        print(f"   • Mediana: {eta_stats['50%']:.1f} anni")
        print(f"   • Range: {eta_stats['min']:.0f}-{eta_stats['max']:.0f} anni")
    
    # Statistiche stipendio
    if 'Salary' in df.columns:
        salary_stats = df['Salary'].describe()
        print(f"\\n💰 **Statistiche Stipendio**:")
        print(f"   • Media: €{salary_stats['mean']:,.0f}")
        print(f"   • Mediana: €{salary_stats['50%']:,.0f}")
        print(f"   • Range: €{salary_stats['min']:,.0f}-€{salary_stats['max']:,.0f}")
    
    # Dipartimenti principali
    if 'Department' in df.columns:
        dept_counts = df['Department'].value_counts().head(5)
        print(f"\\n🏢 **Top 5 Dipartimenti**:")
        for dept, count in dept_counts.items():
            pct = count / total_employees * 100
            print(f"   • {dept}: {count:,} ({pct:.1f}%)")
""")
    
    # Cella collegamenti ai moduli
    cella_moduli = crea_cella_markdown("""
## 📋 Moduli di Analisi Specializzati

Questo dashboard fornisce una panoramica generale. Per analisi approfondite, utilizza i moduli specializzati:

### 🎯 **Moduli Disponibili:**

1. **📊 [Analisi Demografica](./01_Analisi_Demografica.ipynb)**
   - Distribuzione per età, genere, stato civile
   - Fasce generazionali e trend demografici
   - Raccomandazioni per diversity & inclusion

2. **💰 [Analisi Retributiva](./02_Analisi_Retributiva.ipynb)**
   - Distribuzione stipendi per ruolo e dipartimento
   - Gender pay gap e analisi equità
   - Correlazioni anzianità-stipendio

3. **🔄 [Analisi Turnover](./03_Analisi_Turnover.ipynb)**
   - Tassi di turnover per genere e dipartimento
   - Analisi retention e cause di uscita
   - Raccomandazioni per migliorare retention

4. **🏖️ [Proiezioni Pensionistiche](./04_Proiezioni_Pensionistiche.ipynb)**
   - Calcoli secondo leggi italiane
   - Impatto economico e knowledge at risk
   - Pianificazione successione

5. **📈 [Performance Analysis](./05_Performance_Analysis.ipynb)**
   - Distribuzione performance scores
   - Correlazioni con altri fattori
   - Identificazione talenti e aree di miglioramento

6. **📋 [Report Esecutivo](./06_Report_Esecutivo.ipynb)**
   - Sintesi KPI principali
   - Dashboard per leadership
   - Raccomandazioni strategiche

### 🚀 **Come Utilizzare:**
1. Esegui questo dashboard per la panoramica generale
2. Apri i moduli specifici per analisi dettagliate
3. Utilizza il Report Esecutivo per presentazioni alla leadership
""")
    
    # Cella visualizzazione rapida
    cella_viz_rapida = crea_cella_codice("""
# 📊 VISUALIZZAZIONI RAPIDE
if df is not None:
    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    fig.suptitle('HR Dashboard - Panoramica Rapida', fontsize=16, fontweight='bold')
    
    # Grafico 1: Distribuzione per genere
    if 'Gender' in df.columns:
        gender_counts = df['Gender'].value_counts()
        axes[0,0].pie(gender_counts.values, labels=['Uomini' if x=='M' else 'Donne' for x in gender_counts.index], 
                     autopct='%1.1f%%', startangle=90, colors=['lightblue', 'lightcoral'])
        axes[0,0].set_title('Distribuzione per Genere')
    
    # Grafico 2: Distribuzione età
    if 'Eta' in df.columns:
        df['Eta'].hist(bins=15, ax=axes[0,1], alpha=0.7, color='skyblue', edgecolor='black')
        axes[0,1].set_title('Distribuzione Età')
        axes[0,1].set_xlabel('Età')
        axes[0,1].set_ylabel('Numero Dipendenti')
    
    # Grafico 3: Top dipartimenti
    if 'Department' in df.columns:
        dept_counts = df['Department'].value_counts().head(6)
        dept_counts.plot(kind='bar', ax=axes[0,2], color='lightgreen', alpha=0.7)
        axes[0,2].set_title('Top Dipartimenti')
        axes[0,2].set_xlabel('Dipartimento')
        axes[0,2].set_ylabel('Numero Dipendenti')
        axes[0,2].tick_params(axis='x', rotation=45)
    
    # Grafico 4: Distribuzione stipendi
    if 'Salary' in df.columns:
        df['Salary'].hist(bins=15, ax=axes[1,0], alpha=0.7, color='gold', edgecolor='black')
        axes[1,0].set_title('Distribuzione Stipendi')
        axes[1,0].set_xlabel('Stipendio (€)')
        axes[1,0].set_ylabel('Numero Dipendenti')
    
    # Grafico 5: Anzianità di servizio
    if 'AnniServizio' in df.columns:
        df['AnniServizio'].hist(bins=15, ax=axes[1,1], alpha=0.7, color='orange', edgecolor='black')
        axes[1,1].set_title('Anzianità di Servizio')
        axes[1,1].set_xlabel('Anni di Servizio')
        axes[1,1].set_ylabel('Numero Dipendenti')
    
    # Grafico 6: Status dipendenti (se presente)
    if 'EmploymentStatus' in df.columns:
        status_counts = df['EmploymentStatus'].value_counts()
        axes[1,2].pie(status_counts.values, labels=status_counts.index, 
                     autopct='%1.1f%%', startangle=90, colors=['lightgreen', 'lightcoral'])
        axes[1,2].set_title('Status Dipendenti')
    else:
        # Performance scores come alternativa
        if 'PerformanceScore' in df.columns:
            perf_counts = df['PerformanceScore'].value_counts()
            perf_counts.plot(kind='bar', ax=axes[1,2], color='purple', alpha=0.7)
            axes[1,2].set_title('Performance Scores')
            axes[1,2].tick_params(axis='x', rotation=45)
    
    plt.tight_layout()
    plt.show()
    
    print("\\n🎯 Per analisi dettagliate, utilizza i moduli specializzati!")
""")
    
    # Aggiungi le celle al notebook
    notebook["cells"].extend([
        cella_caricamento,
        cella_panoramica,
        cella_moduli,
        cella_viz_rapida
    ])
    
    return notebook

def salva_notebook(notebook, nome_file):
    """Salva il notebook su file."""
    
    with open(nome_file, 'w', encoding='utf-8') as f:
        json.dump(notebook, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Notebook salvato: {nome_file}")

def crea_sistema_modulare():
    """Crea l'intero sistema modulare di notebook."""
    
    print("🚀 CREAZIONE SISTEMA MODULARE HR ANALYTICS")
    print("=" * 60)
    
    # 1. Dashboard principale
    dashboard = crea_notebook_dashboard()
    salva_notebook(dashboard, "00_HR_Dashboard_Principale.ipynb")
    
    # 2. Lista dei moduli da creare
    moduli = [
        {
            "file": "01_Analisi_Demografica.ipynb",
            "titolo": "📊 Analisi Demografica HR",
            "descrizione": "Analisi completa della composizione demografica della forza lavoro."
        },
        {
            "file": "02_Analisi_Retributiva.ipynb", 
            "titolo": "💰 Analisi Retributiva e Pay Equity",
            "descrizione": "Analisi stipendi, gender pay gap e correlazioni retributive."
        },
        {
            "file": "03_Analisi_Turnover.ipynb",
            "titolo": "🔄 Analisi Turnover e Retention", 
            "descrizione": "Analisi tassi di turnover, retention e raccomandazioni."
        },
        {
            "file": "04_Proiezioni_Pensionistiche.ipynb",
            "titolo": "🏖️ Proiezioni Pensionistiche Italia",
            "descrizione": "Calcoli pensionistici secondo normativa italiana e pianificazione successione."
        },
        {
            "file": "05_Performance_Analysis.ipynb",
            "titolo": "📈 Analisi Performance e Talenti",
            "descrizione": "Analisi performance, identificazione talenti e aree di sviluppo."
        },
        {
            "file": "06_Report_Esecutivo.ipynb",
            "titolo": "📋 Report Esecutivo HR",
            "descrizione": "Sintesi KPI e raccomandazioni strategiche per la leadership."
        }
    ]
    
    # Crea i notebook base per ogni modulo
    for modulo in moduli:
        notebook = crea_notebook_vuoto(modulo["titolo"], modulo["descrizione"])
        
        # Aggiungi cella di importazione dati comune
        cella_import = crea_cella_codice("""
# 📁 Importazione dati dal dashboard principale
# Esegui prima il dashboard principale per caricare i dati

try:
    # Verifica se i dati sono già caricati
    if 'df' in globals():
        print(f"✅ Dati già disponibili: {len(df)} dipendenti")
    else:
        # Carica i dati direttamente
        exec(open('carica_dati_hr.py').read())
        print(f"✅ Dati caricati: {len(df)} dipendenti")
except:
    print("⚠️  Esegui prima il dashboard principale (00_HR_Dashboard_Principale.ipynb)")
    print("   oppure carica manualmente i dati HR")
""")
        
        notebook["cells"].append(cella_import)
        
        # Aggiungi placeholder per contenuto specifico
        placeholder = crea_cella_markdown(f"""
## 🚧 Contenuto in Sviluppo

Questo modulo conterrà:

{modulo["descrizione"]}

### 📋 Sezioni Pianificate:
- Caricamento e preparazione dati
- Analisi esplorativa
- Visualizzazioni interattive
- Insight dinamici
- Raccomandazioni actionable

### 🔗 Collegamenti:
- [← Torna al Dashboard](./00_HR_Dashboard_Principale.ipynb)
- [Prossimo Modulo →](./{moduli[(moduli.index(modulo) + 1) % len(moduli)]["file"]})
""")
        
        notebook["cells"].append(placeholder)
        salva_notebook(notebook, modulo["file"])
    
    # Crea file di utilità
    crea_file_utilita()
    
    print(f"\n🎉 Sistema modulare creato con successo!")
    print(f"📁 File creati:")
    print(f"   • 00_HR_Dashboard_Principale.ipynb (Dashboard)")
    for modulo in moduli:
        print(f"   • {modulo['file']}")
    print(f"   • carica_dati_hr.py (Utilità)")
    
    return True

def crea_file_utilita():
    """Crea file di utilità per il sistema modulare."""
    
    # File per caricamento dati condiviso
    codice_caricamento = '''
"""
Utilità condivisa per il caricamento dati HR.
Utilizzato da tutti i moduli del sistema.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def carica_dati_hr():
    """Carica e prepara i dati HR per l'analisi."""
    
    try:
        # Prova prima il dataset con turnover
        df = pd.read_csv('hr_data_con_turnover.csv')
        print(f"✅ Dataset con turnover caricato: {len(df)} dipendenti")
        dataset_type = "turnover"
    except FileNotFoundError:
        try:
            # Fallback al dataset originale
            df = pd.read_csv('hr_data.csv')
            print(f"✅ Dataset originale caricato: {len(df)} dipendenti")
            dataset_type = "originale"
        except FileNotFoundError:
            print("❌ Nessun dataset trovato!")
            return None, None
    
    # Converti le date
    date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')
    
    # Calcola età e anzianità
    oggi = pd.Timestamp.now()
    if 'DateOfBirth' in df.columns:
        eta_days = (oggi - df['DateOfBirth']).dt.days
        df['Eta'] = (eta_days / 365.25).round().astype('Int64')
    
    if 'HiringDate' in df.columns:
        servizio_days = (oggi - df['HiringDate']).dt.days
        df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')
        df['AnnoAssunzione'] = df['HiringDate'].dt.year
    
    return df, dataset_type

# Carica automaticamente i dati quando il file viene importato
if __name__ == "__main__":
    df, dataset_type = carica_dati_hr()
    print(f"📊 Dati HR pronti per l'analisi!")
'''
    
    with open('carica_dati_hr.py', 'w', encoding='utf-8') as f:
        f.write(codice_caricamento)
    
    print("✅ File utilità creato: carica_dati_hr.py")

if __name__ == "__main__":
    crea_sistema_modulare()
