import pandas as pd
import numpy as np

def check_date_issues():
    """Controlla problemi specifici con le date nel file CSV."""
    print("🔍 Controllo dettagliato delle date nel file hr_data.csv...")
    
    # Carica il file
    df = pd.read_csv('hr_data.csv')
    print(f"📊 Dataset caricato: {len(df)} righe")
    
    # Controlla le colonne date
    date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']
    
    for col in date_columns:
        if col in df.columns:
            print(f"\n📅 Analisi colonna: {col}")
            
            # Mostra alcuni valori raw
            print(f"   Primi 5 valori raw: {df[col].head().tolist()}")
            
            # Controlla pattern problematici
            problematic = df[df[col].astype(str).str.contains(',', na=False)]
            if len(problematic) > 0:
                print(f"   ❌ Trovate {len(problematic)} righe con virgole:")
                for idx, row in problematic.iterrows():
                    print(f"      Riga {idx+2}: {row[col]}")
            else:
                print(f"   ✅ Nessuna virgola trovata")
            
            # Prova conversione
            try:
                converted = pd.to_datetime(df[col], errors='coerce')
                nan_count = converted.isna().sum()
                print(f"   📈 Conversione datetime: {len(df) - nan_count}/{len(df)} successi")
                if nan_count > 0:
                    print(f"   ⚠️  {nan_count} valori non convertibili:")
                    problematic_values = df[converted.isna()][col].unique()
                    for val in problematic_values[:10]:  # Mostra max 10
                        print(f"      '{val}'")
            except Exception as e:
                print(f"   ❌ Errore conversione: {e}")

if __name__ == "__main__":
    check_date_issues()
