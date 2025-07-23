"""
Script per correggere l'errore 'titolo' in tutti i notebook.
"""

import json
import os

def correggi_notebook(nome_file, titolo_corretto):
    """Corregge l'errore titolo in un notebook."""
    
    if not os.path.exists(nome_file):
        print(f"❌ {nome_file} non trovato")
        return False
    
    try:
        # Carica il notebook
        with open(nome_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        # Cerca e correggi l'errore nelle celle
        correzioni = 0
        
        for cella in notebook.get('cells', []):
            if cella.get('cell_type') == 'code':
                source = cella.get('source', [])
                
                # Cerca la riga con l'errore
                for i, riga in enumerate(source):
                    if 'print(f\'📊 {titolo}' in riga:
                        # Correggi la riga
                        source[i] = f"print('📊 {titolo_corretto} - Setup completato!')"
                        correzioni += 1
                        break
        
        # Salva il notebook corretto
        if correzioni > 0:
            with open(nome_file, 'w', encoding='utf-8') as f:
                json.dump(notebook, f, indent=2, ensure_ascii=False)
            
            print(f"✅ {nome_file}: {correzioni} correzioni")
            return True
        else:
            print(f"ℹ️  {nome_file}: nessun errore trovato")
            return True
            
    except Exception as e:
        print(f"❌ Errore in {nome_file}: {e}")
        return False

def correggi_tutti_notebook():
    """Corregge l'errore titolo in tutti i notebook."""
    
    print("🔧 CORREZIONE ERRORE 'titolo' IN TUTTI I NOTEBOOK")
    print("=" * 55)
    
    # Lista dei notebook con i titoli corretti
    notebooks = [
        ("00_HR_Dashboard_Principale.ipynb", "HR Analytics Dashboard"),
        ("01_Analisi_Demografica.ipynb", "Analisi Demografica HR"),
        ("02_Analisi_Retributiva.ipynb", "Analisi Retributiva e Pay Equity"),
        ("03_Analisi_Turnover.ipynb", "Analisi Turnover e Retention"),
        ("04_Proiezioni_Pensionistiche.ipynb", "Proiezioni Pensionistiche Italia"),
        ("05_Performance_Analysis.ipynb", "Analisi Performance e Talenti"),
        ("06_Report_Esecutivo.ipynb", "Report Esecutivo HR")
    ]
    
    successi = 0
    
    for nome_file, titolo in notebooks:
        if correggi_notebook(nome_file, titolo):
            successi += 1
    
    print(f"\n🎉 **CORREZIONE COMPLETATA:**")
    print(f"   ✅ {successi}/{len(notebooks)} notebook corretti")
    
    if successi == len(notebooks):
        print(f"   🚀 Tutti i notebook sono ora pronti per l'uso!")
        print(f"   📊 Riprova a eseguire il Dashboard Principale")
    else:
        print(f"   ⚠️  Alcuni notebook potrebbero avere ancora problemi")
    
    return successi == len(notebooks)

if __name__ == "__main__":
    correggi_tutti_notebook()
