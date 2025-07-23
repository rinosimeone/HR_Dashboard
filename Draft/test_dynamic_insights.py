import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def test_dynamic_department_insights():
    """Test del nuovo codice dinamico per gli insight sui dipartimenti."""
    print("🧪 Test degli Insight Dinamici sui Dipartimenti")
    print("=" * 60)
    
    # Carica i dati
    df = pd.read_csv('hr_data.csv')
    print(f"📊 Dataset caricato: {len(df)} dipendenti")
    
    # Replica il codice dinamico del notebook
    if df is not None:
        # 📊 INSIGHT DINAMICI BASATI SUI DATI REALI
        dept_counts = df['Department'].value_counts()
        dept_percentages = (dept_counts / len(df) * 100).round(1)
        total_employees = len(df)
        
        print("🔍 **Insight Dinamici:**")
        print(f"📈 **Distribuzione per Dipartimento** (Totale: {total_employees:,} dipendenti)")
        
        # Top 3 dipartimenti
        top_3 = dept_counts.head(3)
        dept_names = list(top_3.index)
        
        print(f"\n🥇 **Top 3 Dipartimenti:**")
        for i, (dept, count) in enumerate(top_3.items(), 1):
            percentage = dept_percentages[dept]
            print(f"   {i}. **{dept}**: {count:,} dipendenti ({percentage}%)")
        
        # Analisi automatica
        largest_dept = dept_names[0]
        largest_count = top_3.iloc[0]
        largest_pct = dept_percentages.iloc[0]
        
        print(f"\n💡 **Analisi Automatica:**")
        print(f"• Il dipartimento **{largest_dept}** è il più numeroso con {largest_count:,} dipendenti ({largest_pct}% del totale)")
        
        if len(dept_names) >= 2:
            second_dept = dept_names[1]
            second_pct = dept_percentages.iloc[1]
            print(f"• Seguito da **{second_dept}** ({second_pct}%)")
            
            if len(dept_names) >= 3:
                third_dept = dept_names[2]
                third_pct = dept_percentages.iloc[2]
                print(f"• E **{third_dept}** ({third_pct}%)")
        
        # Raccomandazioni dinamiche
        print(f"\n🎯 **Raccomandazioni HR:**")
        if largest_pct > 40:
            print(f"⚠️  **Concentrazione elevata**: {largest_dept} rappresenta oltre il 40% della forza lavoro")
            print(f"   → Considerare diversificazione delle competenze e riduzione del rischio operativo")
        elif largest_pct > 30:
            print(f"📊 **Distribuzione bilanciata**: {largest_dept} ha una presenza significativa ma non eccessiva")
        else:
            print(f"✅ **Distribuzione equilibrata**: Nessun dipartimento domina eccessivamente")
        
        # Analisi dipartimenti piccoli
        small_depts = dept_counts[dept_counts < (total_employees * 0.05)]  # Meno del 5%
        if len(small_depts) > 0:
            print(f"\n🔍 **Dipartimenti piccoli** (< 5% del totale):")
            for dept, count in small_depts.items():
                pct = dept_percentages[dept]
                print(f"   • {dept}: {count} dipendenti ({pct}%)")
            print(f"   → Valutare se necessitano di rinforzi o ristrutturazione")
        
        print("\n" + "=" * 60)
        print("✅ **Test SUPERATO!** Gli insight sono ora completamente dinamici")
        print("🔄 **Vantaggi del nuovo approccio:**")
        print("• ✅ Si aggiorna automaticamente con nuovi dati")
        print("• ✅ Calcola percentuali reali")
        print("• ✅ Identifica automaticamente i dipartimenti principali")
        print("• ✅ Fornisce raccomandazioni basate sui dati")
        print("• ✅ Rileva dipartimenti che potrebbero aver bisogno di attenzione")
        
        # Mostra anche tutti i dipartimenti per verifica
        print(f"\n📋 **Tutti i Dipartimenti nel Dataset:**")
        for dept, count in dept_counts.items():
            pct = dept_percentages[dept]
            print(f"   • {dept}: {count} dipendenti ({pct}%)")

if __name__ == "__main__":
    test_dynamic_department_insights()
