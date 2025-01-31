# Documentazione dell'applicazione "Registro Studenti"

**Versione**: 11.0 (2025.01.31)  
**Autori**: IZ4APU e ChatGPT O1  

L’applicazione descritta dal codice serve per gestire un gruppo di studio, consentendo di registrare informazioni sugli studenti, aggiornare punteggi relativi a diverse attività (es. presenza online, esercizi svolti, commenti, aiuti forniti) e generare un report finale in formato testo.

---

## Struttura e Funzionamento

1. **File di dati**  
   - Il file `Scacchierando - registro_studenti.json` viene utilizzato per caricare e salvare in maniera persistente le informazioni sugli studenti (punteggi, note, ecc.).
   - Se il file non esiste all’avvio, l’applicazione ne creerà uno vuoto.

2. **Caricamento e salvataggio dei dati**  
   - `carica_dati()`: verifica se il file di dati esiste, in caso affermativo lo legge e restituisce un dizionario Python con le informazioni degli studenti.  
   - `salva_dati(dati)`: salva il dizionario `dati` (che contiene tutte le informazioni aggiornate) nel file JSON in modo ordinato (con indentazione).

3. **Funzione `index_to_letter(index)`**  
   - Converte un indice numerico (partendo da 0) in una sequenza di lettere nello stile delle colonne Excel.  
   - Esempio: 0 → A, 1 → B, …, 25 → Z, 26 → AA, 27 → AB, e così via.  
   - Questa funzione è utilizzata per elencare le note degli studenti in maniera “alfabetica”.

4. **Generazione del report**  
   - `genera_report(dati)`: crea un report testuale elencando le “classifiche” degli studenti rispetto a quattro parametri:  
     1. **Risolutori**: punteggi sul totale esercizi svolti.  
     2. **Collaboratori**: punteggi sugli aiuti forniti ad altri.  
     3. **Commentatori**: punteggi sui commenti forniti.  
     4. **Presenze Online**: punteggi sulle presenze registrate nelle sessioni online.  

   - All’interno di ciascuna classifica, viene calcolata la media basata sul rapporto tra “totale” e “valutazioni” (ossia il numero di volte in cui lo studente ha ricevuto un punteggio su quel parametro).
   - La quinta sezione del report (`NOTE DEGLI STUDENTI`) elenca eventuali annotazioni inserite per ciascuno studente, suddivise in punti A, B, C, … (o AA, AB, …) a seconda del numero di note inserite.  
   - Il report finale viene salvato in un file di testo:  
     ```
     e:/dropbox/scacchierando/Risorse e curiosità/Il giochino - Classifiche.txt
     ```
   - Alla fine, un messaggio segnala la generazione di `report_finale.txt` (in questo codice, sembra essere un riferimento, ma il contenuto effettivo è scritto nel file qui sopra).

5. **Ricerca corrispondenze**  
   - `trova_corrispondenze(dati, nome)`: data una stringa `nome`, restituisce un elenco di studenti i cui nomi contengono la stringa ricercata (case-insensitive).  
   - Viene usata per cercare studenti già esistenti nei dati ed evitare duplicati.

6. **Funzione `main()` e flusso principale**  
   - Carica i dati esistenti tramite `carica_dati()`.  
   - Mentre l’utente non scrive “FINE”, l’applicazione continua a chiedere il nome dello studente da aggiornare o aggiungere.
   - Se trova più corrispondenze per un nome parziale, chiede di specificare meglio.  
   - Se non trova corrispondenze, propone di inserire un nuovo studente.  
   - Per ogni studente selezionato, mostra diverse opzioni:  
     1. Aggiornare “Presenze online”  
     2. Aggiornare “Esercizi”  
     3. Aggiornare “Commenti”  
     4. Aggiornare “Aiuto”  
     5. Aggiungere una “Nota”  
     6. [0] per eliminare lo studente.  
   - Il punteggio inserito può essere un numero (anche negativo, nella fascia da -5 a 5).  
   - “Nota” viene accodata alla voce “Note” dello studente, preceduta dalla data corrente.  
   - Quando l’utente digita “FINE”, l’applicazione:  
     1. Genera il report tramite `genera_report(dati)`.  
     2. Salva i dati aggiornati con `salva_dati(dati)`.  
     3. Termina l’esecuzione.

---

## Descrizione dei campi nei dati

Ogni studente, nel file JSON, ha la seguente struttura a dizionario:
```json
{
  "NomeStudente": {
    "Presenze online": {
      "totale": 0,
      "valutazioni": 0
    },
    "Esercizi": {
      "totale": 0,
      "valutazioni": 0
    },
    "Commenti": {
      "totale": 0,
      "valutazioni": 0
    },
    "Aiuto": {
      "totale": 0,
      "valutazioni": 0
    },
    "Note": ""
  }
}
```
- **totale**: somma dei punteggi inseriti.  
- **valutazioni**: numero di volte che si è assegnato un punteggio su quel parametro.  
- **Note**: testo libero, dove ogni nuova nota viene appesa in una riga distinta, con data di inserimento.

---

## Utilizzo dell’app (flusso CLI semplificato)

1. **Avvio**  
   - Eseguire lo script Python (`main()` è il punto di ingresso).  
2. **Inserimento nominativo**  
   - Scrivere il nome dello studente. Se esistono già corrispondenze, l’app le segnala.  
   - Se non esiste, propone di aggiungerlo.  
3. **Selezione opzione**  
   - `1`: aggiunge/rimuove punti al campo “Presenze online”.  
   - `2`: aggiunge/rimuove punti al campo “Esercizi”.  
   - `3`: aggiunge/rimuove punti al campo “Commenti”.  
   - `4`: aggiunge/rimuove punti al campo “Aiuto”.  
   - `5`: aggiunge una nota testuale con la data corrente.  
   - `0`: elimina lo studente dall’archivio.  
4. **Terminazione**  
   - Digitare “FINE” come nome studente per:  
     1. Generare il report.  
     2. Salvare i dati.  
     3. Uscire dal programma.

---

## Esecuzione e Dipendenze

- **Dipendenze principali**:  
  - `json`, `os`, `datetime` (librerie standard di Python)  
  - `GBUtils` (da cui si importa `key`, funzione di input personalizzato)  
  - È necessario che la libreria `GBUtils` sia presente nel path.

- **Esecuzione**  
  1. Assicurarsi di avere Python 3 installato.  
  2. Posizionarsi nella directory contenente lo script (`.py`) ed eseguire:  
     ```bash
     python nome_script.py
     ```
  3. Seguire le istruzioni a schermo.

- **File generati**:  
  - `Scacchierando - registro_studenti.json` (registro dati in formato JSON).  
  - `e:/dropbox/scacchierando/Risorse e curiosità/Il giochino - Classifiche.txt` (report testuale generato).  
  - A schermo viene segnalata anche la creazione di `report_finale.txt` (in base al messaggio di print finale, anche se il contenuto va effettivamente su *Il giochino - Classifiche.txt*).

---

## Possibili Personalizzazioni

- **Percorso del file JSON**: modificare la costante `DATA_FILE` se si desidera salvare in una posizione diversa.  
- **Percorso del file di report**: modificare la stringa nel metodo `genera_report` in base alle proprie preferenze.  
- **Interazione utente**: attualmente basata su `key()` (probabilmente funzione custom in `GBUtils`). È possibile adattarla o sostituirla con un normale `input()`.  
- **Struttura del report**: personalizzare ordine, titolo delle classifiche e formattazione delle note, a seconda delle esigenze.  

---

## Esempio di Report

Esempio (indicativo) di alcune righe del file report:

```
# 2025.02.01 15:30:12 CLASSIFICHE DEGLI STUDENTI (5).

## CLASSIFICA RISOLUTORI.
Pos.: (Valutazioni) Nome: Punti: Media:
 1: (3) Maria Rossi: 7: 2.33
 2: (1) Luca Bianchi: 5: 5.00
 ...

## NOTE DEGLI STUDENTI.

1. Luca Bianchi
    A. 2025.01.31: Ha chiesto di ripassare l’argomento “Algebra”
    B. 2025.02.01: Ha commentato positivamente la lezione di oggi

2. Maria Rossi
    A. 2025.02.01: Ottima collaborazione nel gruppo
```

---

## Conclusioni

Questo script offre un’interfaccia a riga di comando per tenere traccia delle attività e delle note di un gruppo di studio. È pensato per essere semplice e leggero, salvando i dati in formato JSON e producendo un report finale che aiuta a valutare la partecipazione dei vari membri.

Per qualsiasi integrazione o modifica, è sufficiente intervenire direttamente sulle funzioni principali (in particolare `main()`, `genera_report()` e `carica_dati()/salva_dati()`), adattandole alle specifiche esigenze del gruppo di studio.
```