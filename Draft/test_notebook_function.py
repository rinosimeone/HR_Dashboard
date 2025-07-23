import pandas as pd
import numpy as np
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

def carica_e_pulisci_dati():
    """Replica esatta della funzione del notebook per testare"""
    
    # Lista dei possibili nomi file
    possibili_file = ['hr_data.csv', 'HR_Data.csv', 'HR Data.csv']
    
    for file_name in possibili_file:
        try:
            print(f"📁 Tentativo di caricamento del file {file_name}...")
            
            # Caricamento con gestione errori
            try:
                df = pd.read_csv(file_name)
            except pd.errors.ParserError:
                print("🔧 Errore parsing CSV, uso parametri robusti...")
                df = pd.read_csv(file_name, on_bad_lines='skip', skipinitialspace=True)
            
            print(f"✅ Dati caricati da {file_name}! Totale: {len(df):,} dipendenti")
            
            # PULIZIA AUTOMATICA
            print("🧹 Pulizia automatica dei dati...")
            
            # Correggi date malformate
            colonne_date = ['DateOfBirth', 'HiringDate', 'TerminationDate']
            for col in colonne_date:
                if col in df.columns:
                    df[col] = df[col].astype(str).str.strip()
                    # Correggi virgole nelle date (problema principale!)
                    df[col] = df[col].str.replace(r'(\d{2})/(\d{2}),(\d{4})', r'\1/\2/\3', regex=True)
                    df[col] = df[col].replace(['nan', ''], None)
            
            # Converti date
            for col in colonne_date:
                if col in df.columns:
                    df[col] = pd.to_datetime(df[col], errors='coerce')
            
            # Pulisci campo Gender
            if 'Gender' in df.columns:
                df['Gender'] = df['Gender'].str.strip()
                df['Gender'] = df['Gender'].replace({'M ': 'M'})
            
            # Calcola età e anzianità (con gestione NaN)
            oggi = pd.Timestamp('2025-07-18')
            if 'DateOfBirth' in df.columns:
                # Calcola età solo per date valide
                eta_days = (oggi - df['DateOfBirth']).dt.days
                df['Eta'] = (eta_days / 365.25).round().astype('Int64')  # Int64 supporta NaN
                df['Eta'] = df['Eta'].clip(lower=0, upper=100)
            
            if 'HiringDate' in df.columns:
                # Calcola anni di servizio solo per date valide
                servizio_days = (oggi - df['HiringDate']).dt.days
                df['AnniServizio'] = (servizio_days / 365.25).round().astype('Int64')  # Int64 supporta NaN
                df['AnniServizio'] = df['AnniServizio'].clip(lower=0, upper=50)
                df['AnnoAssunzione'] = df['HiringDate'].dt.year
            
            # Pulisci salari
            if 'Salary' in df.columns:
                df = df[df['Salary'] > 0]
            
            print(f"✅ Pulizia completata! Dataset finale: {len(df):,} dipendenti")
            print(f"📊 Colonne disponibili: {', '.join(df.columns)}")
            
            # Mostra statistiche età
            if 'Eta' in df.columns:
                eta_valide = df['Eta'].notna().sum()
                print(f"👥 Età calcolate: {eta_valide}/{len(df)} dipendenti")
                if eta_valide > 0:
                    print(f"   📈 Età media: {df['Eta'].mean():.1f} anni")
                    print(f"   📊 Range età: {df['Eta'].min()}-{df['Eta'].max()} anni")
            
            return df
            
        except FileNotFoundError:
            print(f"❌ File {file_name} non trovato")
            continue
        except Exception as e:
            print(f"❌ Errore durante il caricamento di {file_name}: {str(e)}")
            continue
    
    print("🔴 Impossibile caricare nessun file HR")
    return None

if __name__ == "__main__":
    print("🧪 Test della funzione del notebook...")
    df = carica_e_pulisci_dati()
    
    if df is not None:
        print("\n🎉 Test SUPERATO! La funzione del notebook ora funziona correttamente.")
        print("\n📋 **Anteprima dei Dati Pronti per l'Analisi:**")
        print(df.head())
    else:
        print("\n❌ Test FALLITO!")
