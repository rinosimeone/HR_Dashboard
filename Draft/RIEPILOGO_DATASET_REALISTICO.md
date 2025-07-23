# 🎯 Dataset HR Realistico - Caratteristiche e Analisi

## 📊 **Nuovo Dataset Creato: `hr_data_con_turnover.csv`**

Ho creato un dataset HR completamente nuovo che riflette **tutte le caratteristiche richieste** per un'analisi realistica di un'azienda italiana con problematiche HR critiche.

---

## ✅ **Caratteristiche Implementate**

### 1. **🚹 Maggioranza Maschile**
- **Dipendenti Attivi**: 70% uomini (105), 30% donne (45)
- **Situazione**: Tipica di aziende manifatturiere italiane
- **Impatto**: Squilibrio di genere nella forza lavoro attiva

### 2. **🏖️ Molti Prossimi alla Pensione (Leggi Italiane)**
- **Pensione a 67 anni** (vecchiaia)
- **Pensione anticipata**: 42a10m uomini, 41a10m donne
- **Quota 103**: 62 anni + 41 anni contributi
- **Situazione Critica**: 15-25% va in pensione nei prossimi 5-10 anni

### 3. **📈 Correlazione Anzianità-Stipendio**
- **Correlazione forte**: r > 0.5
- **Formula**: Stipendio base + (800€ × anni anzianità)
- **Variazioni**: Bonus ruolo e differenze per genere

### 4. **⚖️ Gender Pay Gap Evidente**
- **Gap significativo**: 15-25% tra uomini e donne
- **Donne**: Guadagnano 75-85% dello stipendio maschile
- **Uomini**: Stipendio pieno + possibili bonus (100-115%)

### 5. **🔄 Alto Turnover Femminile (NUOVO!)**
- **Turnover Uomini**: ~19% (25 su 130 totali)
- **Turnover Donne**: ~62% (75 su 120 totali)
- **Differenza Critica**: 43 punti percentuali!
- **Situazione**: Emergenza retention femminile

---

## 📁 **File Creati**

### 🎯 **Dataset Principale**
- **`hr_data_con_turnover.csv`** - Dataset con 250 dipendenti (150 attivi + 100 usciti)

### 🛠️ **Script di Generazione**
- **`test_turnover_semplice.py`** - Generatore dataset semplificato
- **`genera_dataset_con_turnover.py`** - Generatore complesso (backup)

### 📊 **Script di Analisi**
- **`analisi_turnover_dettagliata.py`** - Analisi completa turnover
- **`modulo_pensioni_italia.py`** - Proiezioni pensionistiche leggi italiane
- **`verifica_dataset_semplice.py`** - Verifica caratteristiche base

---

## 🏖️ **Proiezioni Pensionistiche Italiane - REINTRODOTTE!**

### **Leggi Italiane 2024:**
1. **Pensione di Vecchiaia**: 67 anni
2. **Pensione Anticipata**: 
   - Uomini: 42 anni e 10 mesi di contributi
   - Donne: 41 anni e 10 mesi di contributi
3. **Quota 103**: 62 anni + 41 anni di contributi (fino al 2024)

### **Analisi Implementate:**
- ✅ Calcolo automatico anni alla pensione per ogni modalità
- ✅ Identificazione pensione più vicina per ogni dipendente
- ✅ Proiezioni per dipartimento e impatto economico
- ✅ Knowledge at risk e raccomandazioni strategiche
- ✅ Visualizzazioni complete

---

## 🚨 **Situazioni Critiche Identificate**

### **1. Emergenza Turnover Femminile**
- **62% delle donne** ha lasciato l'azienda
- **Cause potenziali**: Gender pay gap, cultura aziendale, work-life balance
- **Azione richiesta**: Intervento immediato HR

### **2. Gender Pay Gap Significativo**
- **15-25% di differenza** salariale
- **Impatto**: Demotivazione e turnover femminile
- **Azione richiesta**: Revisione politiche retributive

### **3. Rischio Pensionamenti**
- **15-25% va in pensione** nei prossimi 5-10 anni
- **Impatto**: Perdita di knowledge e esperienza
- **Azione richiesta**: Piano di successione urgente

### **4. Squilibrio di Genere**
- **70% uomini** nella forza lavoro attiva
- **Combinato con alto turnover femminile**
- **Rischio**: Ulteriore peggioramento dell'equilibrio

---

## 📊 **Analisi Disponibili**

### **🔄 Analisi Turnover**
```python
# Esegui analisi completa turnover
python analisi_turnover_dettagliata.py
```
- Turnover per genere, dipartimento, età
- Correlazioni stipendio-turnover
- Visualizzazioni complete
- Raccomandazioni dinamiche

### **🏖️ Analisi Pensionistica**
```python
# Esegui analisi proiezioni pensionistiche
python modulo_pensioni_italia.py
```
- Calcoli secondo leggi italiane
- Impatto per dipartimento
- Knowledge at risk
- Pianificazione successione

### **📈 Analisi Correlazioni**
- Anzianità vs Stipendio (r > 0.5)
- Genere vs Stipendio (gap significativo)
- Età vs Turnover (giovani se ne vanno di più)
- Dipartimento vs Retention

---

## 🎯 **Integrazione nel Notebook**

### **Nuove Sezioni da Aggiungere:**

1. **📊 Analisi Turnover per Genere**
   - Tassi di turnover dinamici
   - Identificazione cause
   - Raccomandazioni retention

2. **🏖️ Proiezioni Pensionistiche Italiane**
   - Calcoli secondo normativa
   - Impatto economico
   - Piano di successione

3. **⚖️ Analisi Gender Pay Gap**
   - Gap per fasce di anzianità
   - Correlazioni con turnover
   - Raccomandazioni equity

4. **🔄 Dashboard Retention**
   - KPI turnover in tempo reale
   - Alert per situazioni critiche
   - Trend analysis

---

## 🚀 **Prossimi Passi**

### **1. Integrazione Notebook**
- Aggiungere nuove sezioni al notebook principale
- Implementare insight dinamici per turnover
- Integrare modulo pensioni italiane

### **2. Personalizzazione**
- Adattare soglie alle specifiche aziendali
- Personalizzare dipartimenti e ruoli
- Configurare alert e notifiche

### **3. Automazione**
- Collegare a sistemi HR esistenti
- Automatizzare report mensili
- Implementare dashboard real-time

---

## 💡 **Valore Aggiunto**

### **Per l'HR Manager:**
- **Identificazione proattiva** di problemi critici
- **Dati concreti** per decisioni strategiche
- **Raccomandazioni specifiche** e actionable

### **Per la Leadership:**
- **Visibilità completa** su rischi HR
- **Proiezioni economiche** accurate
- **Piani di azione** basati sui dati

### **Per l'Azienda:**
- **Prevenzione turnover** costoso
- **Pianificazione successione** efficace
- **Miglioramento clima aziendale**

---

## 🎉 **Risultato Finale**

**Un dataset HR realistico che riflette le sfide reali delle aziende italiane:**

- ✅ Maggioranza maschile
- ✅ Molti prossimi alla pensione
- ✅ Correlazione anzianità-stipendio
- ✅ Gender pay gap evidente
- ✅ **BONUS**: Alto turnover femminile critico
- ✅ **BONUS**: Proiezioni pensionistiche leggi italiane

**Pronto per analisi HR avanzate e decision-making strategico!** 🚀

---

*Dataset creato per riflettere situazioni HR reali e critiche che richiedono interventi immediati e pianificazione strategica.*
