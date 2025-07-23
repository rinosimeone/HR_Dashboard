import pandas as pd
import numpy as np

def load_and_preview_hr_data():
    """Load the HR data and show basic information."""
    print("📁 Tentativo di caricamento del file 'hr_data.csv'...")
    
    try:
        # Load the CSV file
        df = pd.read_csv('hr_data.csv')
        print("✅ File caricato con successo!")
        
        # Basic information
        print(f"\n📊 Informazioni sul dataset:")
        print(f"   • Righe: {df.shape[0]}")
        print(f"   • Colonne: {df.shape[1]}")
        
        # Show column names
        print(f"\n📋 Colonne disponibili:")
        for i, col in enumerate(df.columns, 1):
            print(f"   {i:2d}. {col}")
        
        # Show first few rows
        print(f"\n👀 Prime 5 righe del dataset:")
        print(df.head())
        
        # Basic statistics
        print(f"\n📈 Statistiche di base per le colonne numeriche:")
        numeric_cols = df.select_dtypes(include=[np.number]).columns
        if len(numeric_cols) > 0:
            print(df[numeric_cols].describe())
        
        # Check for missing values
        print(f"\n🔍 Valori mancanti per colonna:")
        missing_values = df.isnull().sum()
        for col, missing in missing_values.items():
            if missing > 0:
                print(f"   • {col}: {missing} valori mancanti")
        
        if missing_values.sum() == 0:
            print("   ✅ Nessun valore mancante trovato!")
        
        return df
        
    except Exception as e:
        print(f"❌ Si è verificato un errore durante il caricamento del file: {str(e)}")
        return None

if __name__ == "__main__":
    df = load_and_preview_hr_data()
    if df is not None:
        print(f"\n🎉 Il file è ora pronto per l'analisi!")
