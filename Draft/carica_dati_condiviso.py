"""
File di caricamento dati condiviso per tutti i moduli.
Risolve il problema 'df is not defined'.
"""

import pandas as pd
import numpy as np
from datetime import datetime

def carica_dati_hr():
    """Carica e prepara i dati HR per l'analisi."""
    
    try:
        # Prova prima il dataset con turnover
        df = pd.read_csv('hr_data_con_turnover.csv')
        print(f"Dataset con turnover caricato: {len(df)} dipendenti")
        dataset_type = "turnover"
    except FileNotFoundError:
        try:
            # Fallback al dataset originale
            df = pd.read_csv('hr_data.csv')
            print(f"Dataset originale caricato: {len(df)} dipendenti")
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
    
    print("Dati preparati per l'analisi!")
    return df, dataset_type

# Carica automaticamente i dati quando il file viene importato
if __name__ == "__main__":
    df, dataset_type = carica_dati_hr()
    print("Dati HR pronti per l'analisi!")
else:
    # Quando importato da altri moduli
    df, dataset_type = carica_dati_hr()
