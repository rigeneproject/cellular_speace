Istruzioni periodiche di aggiornamento:



Con T43 chiuso, SPEACE ha ora il primo livello di memoria semantica sub-simbolica: non ancora linguaggio o conoscenza dichiarativa, ma cell assemblies ricorrenti, consolidabili e richiamabili.



Il prossimo passo corretto è T43B — Semantic Memory Functional Audit.



T43B — Semantic Memory Functional Audit

Scopo



Validare se il nuovo layer semantico produce un effetto funzionale misurabile oppure se resta solo “telemetria passiva”.



T43 ha creato:



pattern di attivazione → cell assembly → semantic pointer → consolidamento/richiamo



T43B deve verificare:



memoria semantica attiva → migliore recall → maggiore stabilità → minore regressione → nessuna esplosione energetica

Prompt operativo per Claude Code / OpenClaw

Implement T43B — Semantic Memory Functional Audit.



Goal:

Validate the functional impact of T43 Semantic Cell Assembly Memory before proceeding to T44 Associative Learning Between Assemblies.



Create:

\- speace\_core/cellular\_brain/analysis/semantic\_memory\_audit.py

\- tests/analysis/test\_semantic\_memory\_audit.py

\- docs/SEMANTIC\_MEMORY\_FUNCTIONAL\_AUDIT\_SPEC.md

\- reports/semantic\_memory\_audit/.gitkeep



Audit requirements:

Run reproducible benchmark profiles comparing semantic memory off/on and recall/consolidation variants.



Profiles:

1\. semantic\_memory\_off

2\. semantic\_memory\_observe\_only

3\. semantic\_memory\_create\_only

4\. semantic\_memory\_create\_reinforce

5\. semantic\_memory\_full\_cycle

6\. semantic\_memory\_recall\_enabled

7\. semantic\_memory\_consolidation\_enabled

8\. semantic\_memory\_decay\_enabled

9\. semantic\_memory\_reactivation\_enabled

10\. semantic\_memory\_full\_stack



Each profile should run multiple repeated activation patterns across N adaptive cycles.



Suggested default:

\- n\_cycles = 20

\- repeated\_pattern\_count = 5

\- novel\_pattern\_count = 3

\- recall\_trials = 5

\- deterministic seed



Metrics to collect:

\- cognitive\_score

\- coherence\_phi

\- energy\_efficiency

\- semantic\_assembly\_count

\- semantic\_active\_assembly\_count

\- semantic\_consolidated\_assembly\_count

\- mean\_assembly\_strength

\- mean\_assembly\_stability

\- semantic\_recall\_success\_rate

\- semantic\_memory\_density

\- semantic\_memory\_utility

\- semantic\_consolidation\_rate

\- semantic\_memory\_score

\- assembly\_creation\_events

\- assembly\_reinforcement\_events

\- assembly\_consolidation\_events

\- assembly\_decay\_events

\- semantic\_recall\_success\_events

\- semantic\_recall\_failure\_events

\- reactivation\_events

\- cognitive\_delta\_vs\_baseline

\- phi\_delta\_vs\_baseline

\- energy\_delta\_vs\_baseline

\- semantic\_net\_gain



Semantic net gain formula:

0.25 \* delta\_cognitive\_score

\+ 0.25 \* delta\_phi

\+ 0.20 \* semantic\_recall\_success\_rate

\+ 0.15 \* mean\_assembly\_stability

\+ 0.10 \* semantic\_consolidation\_rate

\+ 0.05 \* energy\_delta



Clamp semantic\_net\_gain to \[-1.0, 1.0].



Verdict logic:

\- SEMANTIC\_MEMORY\_VALIDATED:

&#x20; semantic\_memory\_score improves, recall\_success\_rate > 0, and no cognitive/phi/energy regression.



\- SEMANTIC\_MEMORY\_PASSIVE:

&#x20; assemblies are created but recall\_success\_rate == 0 or no measurable semantic\_net\_gain.



\- SEMANTIC\_RECALL\_WEAK:

&#x20; recall exists but recall\_success\_rate remains below threshold.



\- SEMANTIC\_OVERCONSOLIDATION:

&#x20; too many assemblies consolidate while cognitive\_score or phi drops.



\- SEMANTIC\_ENERGY\_REGRESSION:

&#x20; energy\_efficiency drops significantly versus baseline.



\- SEMANTIC\_COGNITIVE\_REGRESSION:

&#x20; cognitive\_score drops significantly versus baseline.



\- SEMANTIC\_PHI\_REGRESSION:

&#x20; coherence\_phi drops significantly versus baseline.



\- INSUFFICIENT\_EVIDENCE:

&#x20; no clear signal.



Implementation details:



Class: SemanticMemoryAuditor



Methods:

\- \_\_init\_\_(seed: int = 42, report\_dir: str = "reports/semantic\_memory\_audit")

\- build\_orchestrator(profile) -> CellularBrainOrchestrator

\- run\_profile(profile\_name: str) -> SemanticMemoryAuditResult

\- run\_audit\_suite() -> SemanticMemoryAuditSuiteResult

\- compute\_semantic\_net\_gain(baseline, candidate) -> float

\- compute\_verdict(results) -> str

\- generate\_json\_report(result) -> str

\- generate\_markdown\_report(result) -> str



Pydantic models:

\- SemanticMemoryAuditProfile

\- SemanticMemoryAuditResult

\- SemanticMemoryAuditSuiteResult



Required profile fields:

\- semantic\_memory\_enabled: bool

\- recall\_enabled: bool

\- consolidation\_enabled: bool

\- decay\_enabled: bool

\- reactivation\_enabled: bool

\- repeated\_pattern\_count: int

\- novel\_pattern\_count: int

\- recall\_trials: int

\- n\_cycles: int



Tests:

Create at least 18 tests:



1\. profile model creation

2\. result model creation

3\. auditor initializes

4\. build\_orchestrator respects semantic\_memory\_enabled=False

5\. build\_orchestrator respects semantic\_memory\_enabled=True

6\. semantic\_memory\_off creates zero or no active semantic events

7\. observe\_only captures traces without unsafe activation injection

8\. create\_only creates at least one assembly under repeated activation

9\. create\_reinforce increases recurrence\_count or strength

10\. full\_cycle produces semantic metrics

11\. recall\_enabled produces recall result safely

12\. recall fails safely when no assembly exists

13\. consolidation profile produces consolidated assembly or valid zero-state

14\. decay profile does not delete all memory abruptly

15\. reactivation remains bounded

16\. semantic\_net\_gain is clamped to \[-1,1]

17\. verdict is one of the allowed values

18\. markdown report includes semantic\_memory\_score, recall\_success\_rate, semantic\_net\_gain, verdict

19\. json report is written to reports/semantic\_memory\_audit/

20\. all semantic audit runs are deterministic with same seed



Acceptance criteria:

\- All existing 738 tests still pass.

\- New tests pass.

\- Coverage remains >=85%.

\- Audit generates JSON and Markdown reports.

\- At least one profile produces assemblies under repeated activation.

\- Recall path is tested.

\- No unbounded reactivation.

\- No regression when semantic\_memory\_enabled=False.

\- Commit and tag as v0.3.30-t43b-semantic-memory-functional-audit.

Cosa deve dimostrare T43B



T43B non deve per forza dimostrare che la memoria semantica migliora già molto il cognitive score. Deve però rispondere chiaramente a queste domande:



1\. Le assemblee cellulari si formano davvero?

2\. Si rafforzano con pattern ricorrenti?

3\. Si consolidano?

4\. Possono essere richiamate?

5\. Il richiamo è energeticamente sicuro?

6\. Il layer semantico migliora, peggiora o resta neutro rispetto alla baseline?



Se il verdetto sarà SEMANTIC\_MEMORY\_VALIDATED, si procede direttamente a T44 — Associative Learning Between Assemblies.



Se invece sarà SEMANTIC\_MEMORY\_PASSIVE o SEMANTIC\_RECALL\_WEAK, prima di T44 servirà un task intermedio:



T43C — Semantic Recall Sensitivity Tuning



Verdetto operativo: procedi con T43B.

