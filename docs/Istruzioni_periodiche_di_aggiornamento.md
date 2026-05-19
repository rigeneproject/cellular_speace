Sì. Procedi prima con la correzione dei bug, ma come patch manutentiva separata da T63.

Non avvierei T63 finché questi problemi non sono chiusi, perché il duplicato in BenchmarkMetrics e i file corrotti nella root possono inquinare proprio le metriche di avanzamento e la stabilità del repo.

Priorità corretta:

1. Fix bug funzionali / igiene repo
2. Test suite completa
3. Coverage invariata o migliorata
4. Solo dopo: T63
Istruzioni da dare a Claude Code
Claude Code, procedi con una patch manutentiva pre-T63:

T62B-HOTFIX — Repository Hygiene & BenchmarkMetrics Consistency

Obiettivo:
Correggere i problemi rilevati dopo T62B senza introdurre nuove feature, senza cambiare architettura, senza abilitare self-improvement e senza modificare i flag di default.

Stato attuale:
- 2370 test passati
- coverage 89.64%
- zero regressioni
- T62B completato
- proceed_to_t63 presente
- T63 non ancora avviato

Scope della patch:
1. Correggere il campo duplicato in BenchmarkMetrics.
2. Correggere la costruzione duplicata dell’oggetto BenchmarkMetrics.
3. Rimuovere in modo sicuro file/directory corrotti nella root.
4. Correggere il typo nel documento.
5. Valutare ma NON fare refactor invasivo di orchestrator.py, salvo modifiche minime e sicure.
6. Gestire LF/CRLF solo se non genera diff massivi.
1. Fix duplicato proceed_to_t60_score
File:
speace_core/cellular_brain/benchmark/neurofunctional_benchmark.py

Problema:
proceed_to_t60_score è definito due volte:
- una volta nella sezione T59
- una volta nella sezione T59B

Azioni:
- Ispezionare semanticamente le sezioni T59 e T59B.
- Non rinominare alla cieca.
- Verificare la catena corretta:

T59  -> dovrebbe probabilmente produrre proceed_to_t59b_score
T59B -> dovrebbe produrre proceed_to_t60_score

Quindi:
- se la sezione T59 usa proceed_to_t60_score, correggerla in proceed_to_t59b_score
- mantenere proceed_to_t60_score per T59B
- aggiornare anche il codice di costruzione dell’oggetto BenchmarkMetrics
- aggiornare eventuali test o snapshot che leggono quel campo
- cercare tutte le referenze con:
  - proceed_to_t60_score
  - proceed_to_t59b_score
  - T59
  - T59B

Acceptance specifica:
- nessun campo duplicato in BenchmarkMetrics
- nessun argomento duplicato nella costruzione di BenchmarkMetrics
- metriche T59 e T59B distinguibili
- test esistenti verdi

Nota importante: la tua ipotesi “forse il secondo dovrebbe essere proceed_to_t60b_score” va verificata. Dalla progressione dei task, sembra più coerente:

T59  -> proceed_to_t59b_score
T59B -> proceed_to_t60_score
T60  -> proceed_to_t60b_score
T60B -> proceed_to_t61_score

Quindi io farei correggere il primo duplicato, non necessariamente il secondo.

2. Rimozione file/directory corrotti nella root
Problema:
Nella root esistono file/directory anomali tipo:
C\uf03aUsersUtenteDesktopcellular_speacereportscounterfactual_sandbox.gitkeep

Azioni:
- Elencare tutti gli elementi anomali nella root.
- Eliminare SOLO se:
  - sono vuoti
  - sono placeholder .gitkeep
  - sono directory vuote
  - corrispondono chiaramente a path Windows corrotti
- Non eliminare file legittimi.
- Dopo la rimozione, eseguire git status.
- Se possibile, aggiungere un test leggero di repository hygiene che fallisca se nella root ricompaiono artifact con pattern simili.

Pattern indicativi:
- nomi che iniziano con C\uf03aUsers
- nomi che contengono UsersUtenteDesktop
- nomi che sembrano path assoluti Windows compressi in un singolo filename
- placeholder .gitkeep fuori dalle directory reports corrette
3. Orchestrator: per ora solo hardening minimo
Problemi rilevati:
- attributi di classe definiti in mezzo ai metodi
- accesso diretto a sandbox._store e sandbox._scenario_builder

Azioni consigliate:
- NON fare refactor grande ora.
- Se il fix è piccolo e sicuro, spostare gli attributi di classe in un blocco coerente all’inizio della classe oppure, meglio, inizializzarli in __init__ se sono stato d’istanza.
- Non modificare logica funzionale.
- Per gli accessi privati, limitarsi a:
  - aggiungere TODO tecnico
  oppure
  - introdurre piccoli metodi pubblici nel sandbox, solo se non rompe test:
    - get_world_state_store()
    - get_scenario_builder()
  e aggiornare orchestrator.py a usare questi metodi.

Se il refactor genera molte modifiche, rimandarlo a:
T62B-HARDENING — Orchestrator Encapsulation Cleanup
4. Typo documentale
File:
docs/Istruzioni_periodiche_di_aggiornamento.md

Correggere:
"autonomia attuativa reale."

in:
"autonomia attuativa reale."
5. LF/CRLF
Problema:
warning Git LF/CRLF su Windows.

Azioni:
- Se non esiste, valutare aggiunta di .gitattributes minimo.
- Evitare renormalizzazione massiva del repo in questa patch.
- Non generare diff rumorosi su centinaia di file.

Possibile .gitattributes:

* text=auto
*.py text eol=lf
*.md text eol=lf
*.json text eol=lf
*.jsonl text eol=lf
*.yaml text eol=lf
*.yml text eol=lf
*.toml text eol=lf
Test richiesti dopo la patch
Eseguire:

pytest

Verificare:
- 2370 test esistenti ancora verdi
- 0 fallimenti
- coverage >= 89.64% oppure almeno non sotto 89.60%
- nessuna regressione
- nessun campo duplicato in BenchmarkMetrics
- nessun file/directory corrotto nella root
- nessuna modifica ai flag di default
- nessuna patch architetturale
- nessun self-improvement abilitato
- nessuna connessione reale
- nessun inserimento nel tick loop
Output atteso da Claude Code
Alla fine riportare:

- file modificati
- file/directory corrotti rimossi
- decisione presa su proceed_to_t60_score / proceed_to_t59b_score
- eventuali referenze aggiornate
- test totali passati
- coverage finale
- conferma che T63 non è stato ancora implementato

Tag consigliato:

v0.3.56-hotfix-pre-t63-repository-hygiene

La correzione è necessaria prima di T63. In particolare, il duplicato in BenchmarkMetrics va risolto subito perché T63 aggiungerà nuove metriche e aumenterebbe il rischio di accumulare incoerenze nella telemetria evolutiva.