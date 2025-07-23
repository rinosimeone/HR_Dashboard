"""
Script per correggere automaticamente tutti i notebook con il caricamento dati corretto.
"""

import json
import os

def crea_cella_setup_corretta():
    """Crea la cella di setup e caricamento dati corretta."""
    return {
        "cell_type": "code",
        "execution_count": None,
        "metadata": {},
        "outputs": [],
        "source": [
            "# 📁 SETUP E CARICAMENTO DATI\n",
            "import pandas as pd\n",
            "import numpy as np\n",
            "import matplotlib.pyplot as plt\n",
            "import seaborn as sns\n",
            "import warnings\n",
            "warnings.filterwarnings('ignore')\n",
            "\n",
            "# Configurazione grafici\n",
            "plt.style.use('default')\n",
            "sns.set_palette('viridis')\n",
            "plt.rcParams['figure.figsize'] = (12, 8)\n",
            "\n",
            "# Carica dati con encoding corretto\n",
            "try:\n",
            "    df = pd.read_csv('hr_data_con_turnover.csv', encoding='utf-8')\n",
            "    print(f\"Dataset caricato: {len(df)} dipendenti\")\n",
            "    \n",
            "    # Converti date\n",
            "    date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']\n",
            "    for col in date_columns:\n",
            "        if col in df.columns:\n",
            "            df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')\n",
            "    \n",
            "    # Calcola età e anzianità\n",
            "    oggi = pd.Timestamp.now()\n",
            "    if 'DateOfBirth' in df.columns:\n",
            "        eta_days = (oggi - df['DateOfBirth']).dt.days\n",
            "        df['Eta'] = (eta_days / 365.25).round().astype('Int64')\n",
            "    \n",
            "    if 'HiringDate' in df.columns:\n",
            "        servizio_days = (oggi - df['HiringDate']).dt.days\n",
            "        df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')\n",
            "    \n",
            "    print(\"Dati preparati per l'analisi!\")\n",
            "    \n",
            "except UnicodeDecodeError:\n",
            "    # Fallback con encoding diverso\n",
            "    try:\n",
            "        df = pd.read_csv('hr_data_con_turnover.csv', encoding='latin-1')\n",
            "        print(f\"Dataset caricato con encoding latin-1: {len(df)} dipendenti\")\n",
            "        # Ripeti la preparazione dati\n",
            "        date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']\n",
            "        for col in date_columns:\n",
            "            if col in df.columns:\n",
            "                df[col] = pd.to_datetime(df[col], format='%m/%d/%Y', errors='coerce')\n",
            "        oggi = pd.Timestamp.now()\n",
            "        if 'DateOfBirth' in df.columns:\n",
            "            eta_days = (oggi - df['DateOfBirth']).dt.days\n",
            "            df['Eta'] = (eta_days / 365.25).round().astype('Int64')\n",
            "        if 'HiringDate' in df.columns:\n",
            "            servizio_days = (oggi - df['HiringDate']).dt.days\n",
            "            df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')\n",
            "        print(\"Dati preparati per l'analisi!\")\n",
            "    except:\n",
            "        print(\"Errore nel caricamento del dataset\")\n",
            "        df = None\n",
            "except Exception as e:\n",
            "    print(f\"Errore: {e}\")\n",
            "    df = None"
        ]
    }

def correggi_notebook(nome_file):
    """Corregge un singolo notebook."""
    
    if not os.path.exists(nome_file):
        print(f"❌ {nome_file} non trovato")
        return False
    
    try:
        # Carica il notebook
        with open(nome_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Trova e sostituisci la seconda cella (setup)
        if len(notebook.get('cells', [])) >= 2:
            # Sostituisci la seconda cella con quella corretta
            notebook['cells'][1] = crea_cella_setup_corretta()
            
            # Salva il notebook corretto
            with open(nome_file, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {nome_file}: Corretto!")
            return True
        else:
            print(f"⚠️  {nome_file}: Struttura non standard")
            return False
            
    except Exception as e:
        print(f"❌ Errore in {nome_file}: {e}")
        return False

def correggi_tutti_notebook():
    """Corregge tutti i notebook del sistema."""
    
    print("🔧 CORREZIONE AUTOMATICA TUTTI I NOTEBOOK")
    print("=" * 50)
    
    # Lista dei notebook da correggere
    notebooks = [
        "01_Analisi_Demografica.ipynb",
        "02_Analisi_Retributiva.ipynb", 
        "03_Analisi_Turnover.ipynb",
        "04_Proiezioni_Pensionistiche.ipynb",
        "05_Performance_Analysis.ipynb",
        "06_Report_Esecutivo.ipynb"
    ]
    
    successi = 0
    
    for notebook in notebooks:
        if correggi_notebook(notebook):
            successi += 1
    
    print(f"\n🎉 **CORREZIONE COMPLETATA:**")
    print(f"   ✅ {successi}/{len(notebooks)} notebook corretti")
    
    if successi == len(notebooks):
        print(f"   🚀 Tutti i notebook sono ora pronti per l'uso!")
        print(f"   📊 Prova ad aprire qualsiasi modulo specializzato")
        print(f"\n📋 **ORDINE CONSIGLIATO:**")
        print(f"   1. 🎯 00_HR_Dashboard_Principale.ipynb")
        print(f"   2. 🔄 03_Analisi_Turnover.ipynb")
        print(f"   3. 🏖️ 04_Proiezioni_Pensionistiche.ipynb")
        print(f"   4. 💰 02_Analisi_Retributiva.ipynb")
        print(f"   5. 👥 01_Analisi_Demografica.ipynb")
        print(f"   6. 📈 05_Performance_Analysis.ipynb")
        print(f"   7. 📋 06_Report_Esecutivo.ipynb")
    else:
        print(f"   ⚠️  Alcuni notebook potrebbero avere ancora problemi")
    
    return successi == len(notebooks)

if __name__ == "__main__":
    correggi_tutti_notebook()
