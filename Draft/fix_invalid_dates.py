import pandas as pd
import re

def fix_invalid_dates():
    """Corregge le date invalide nel file CSV."""
    print("🔧 Correzione date invalide nel file hr_data.csv...")
    
    # Leggi il file come testo per correzioni precise
    with open('hr_data.csv', 'r', encoding='utf-8') as file:
        content = file.read()
    
    original_content = content
    
    # Correzioni specifiche per date invalide
    corrections = {
        # Date di nascita invalide (29 febbraio in anni non bisestili)
        '02/29/1989': '02/28/1989',  # 1989 non è bisestile
        '02/29/1983': '02/28/1983',  # 1983 non è bisestile  
        '02/29/1981': '02/28/1981',  # 1981 non è bisestile
        
        # Date di assunzione invalide
        '09/09,': '09/09/2020,',     # Data incompleta, assumo 2020
        '02/29/2021': '02/28/2021',  # 2021 non è bisestile
        
        # Date di terminazione invalide
        ',2020,': ',,',              # Rimuovi anno isolato
    }
    
    corrections_made = 0
    
    for invalid_date, valid_date in corrections.items():
        if invalid_date in content:
            content = content.replace(invalid_date, valid_date)
            corrections_made += 1
            print(f"   ✅ Corretto: '{invalid_date}' → '{valid_date}'")
    
    # Salva il file corretto
    if corrections_made > 0:
        with open('hr_data.csv', 'w', encoding='utf-8') as file:
            file.write(content)
        print(f"\n🎉 File corretto! {corrections_made} correzioni applicate.")
    else:
        print("\n✅ Nessuna correzione necessaria.")
    
    # Verifica finale
    print("\n🔍 Verifica finale...")
    df = pd.read_csv('hr_data.csv')
    
    # Test conversioni date
    date_columns = ['DateOfBirth', 'HiringDate', 'TerminationDate']
    for col in date_columns:
        if col in df.columns:
            converted = pd.to_datetime(df[col], errors='coerce')
            valid_count = converted.notna().sum()
            total_non_empty = df[col].notna().sum()
            print(f"   📅 {col}: {valid_count}/{total_non_empty} date valide")

if __name__ == "__main__":
    fix_invalid_dates()
