"""
Verifica lo stato di completamento di tutti i notebook.
"""

import json
import os

def verifica_notebook(nome_file):
    """Verifica il contenuto di un notebook."""
    
    if not os.path.exists(nome_file):
        return "❌ File mancante"
    
    try:
        with open(nome_file, 'r', encoding='utf-8') as f:
            notebook = json.load(f)
        
        celle_totali = len(notebook.get('cells', []))
        celle_codice = len([c for c in notebook['cells'] if c['cell_type'] == 'code'])
        celle_markdown = len([c for c in notebook['cells'] if c['cell_type'] == 'markdown'])
        
        # Verifica se ha contenuto sostanziale (più di 3 celle)
        if celle_totali <= 3:
            return f"⚠️  Base ({celle_totali} celle) - DA COMPLETARE"
        elif celle_totali <= 6:
            return f"📊 Parziale ({celle_totali} celle) - IN SVILUPPO"
        else:
            return f"✅ Completo ({celle_totali} celle: {celle_codice}C + {celle_markdown}M)"
            
    except Exception as e:
        return f"❌ Errore: {e}"

def verifica_tutti_notebook():
    """Verifica tutti i notebook del sistema."""
    
    print("🔍 VERIFICA STATO NOTEBOOK SISTEMA MODULARE")
    print("=" * 55)
    
    notebooks = [
        ("00_HR_Dashboard_Principale.ipynb", "🎯 Dashboard Principale"),
        ("01_Analisi_Demografica.ipynb", "👥 Analisi Demografica"),
        ("02_Analisi_Retributiva.ipynb", "💰 Analisi Retributiva"),
        ("03_Analisi_Turnover.ipynb", "🔄 Analisi Turnover"),
        ("04_Proiezioni_Pensionistiche.ipynb", "🏖️ Proiezioni Pensionistiche"),
        ("05_Performance_Analysis.ipynb", "📈 Performance Analysis"),
        ("06_Report_Esecutivo.ipynb", "📋 Report Esecutivo")
    ]
    
    completi = 0
    parziali = 0
    base = 0
    mancanti = 0
    
    for file_name, descrizione in notebooks:
        stato = verifica_notebook(file_name)
        print(f"{descrizione:.<35} {stato}")
        
        if "✅ Completo" in stato:
            completi += 1
        elif "📊 Parziale" in stato:
            parziali += 1
        elif "⚠️ Base" in stato:
            base += 1
        else:
            mancanti += 1
    
    print(f"\n📊 **RIEPILOGO STATO:**")
    print(f"   ✅ Completi: {completi}/7")
    print(f"   📊 Parziali: {parziali}/7")
    print(f"   ⚠️  Base: {base}/7")
    print(f"   ❌ Mancanti: {mancanti}/7")
    
    # Valutazione generale
    if completi >= 5:
        print(f"\n🎉 **SISTEMA OPERATIVO**: Maggioranza moduli completi!")
        print(f"   🚀 Pronto per l'uso aziendale")
    elif completi >= 3:
        print(f"\n📊 **SISTEMA FUNZIONALE**: Moduli core completi")
        print(f"   🔧 Completare moduli rimanenti per funzionalità complete")
    elif completi >= 1:
        print(f"\n⚠️  **SISTEMA PARZIALE**: Alcuni moduli operativi")
        print(f"   🛠️  Necessario completare sviluppo")
    else:
        print(f"\n🚨 **SISTEMA IN SVILUPPO**: Moduli da completare")
        print(f"   🔨 Sviluppo in corso")
    
    # Raccomandazioni specifiche
    print(f"\n🎯 **RACCOMANDAZIONI:**")
    
    if base > 0:
        print(f"   📝 Completare {base} moduli con struttura base")
    
    if parziali > 0:
        print(f"   🔧 Finalizzare {parziali} moduli parzialmente sviluppati")
    
    if completi >= 2:
        print(f"   ✅ Utilizzare i {completi} moduli completi per analisi immediate")
    
    print(f"\n💡 **PRIORITÀ UTILIZZO:**")
    print(f"   1. 🎯 Dashboard Principale (navigazione)")
    print(f"   2. 🔄 Analisi Turnover (situazione critica)")
    print(f"   3. 🏖️ Proiezioni Pensionistiche (pianificazione)")
    print(f"   4. 💰 Analisi Retributiva (pay gap)")
    print(f"   5. 👥 Analisi Demografica (composizione)")
    print(f"   6. 📈 Performance Analysis (talenti)")
    print(f"   7. 📋 Report Esecutivo (sintesi leadership)")

if __name__ == "__main__":
    verifica_tutti_notebook()
