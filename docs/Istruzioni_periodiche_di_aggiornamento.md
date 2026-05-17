Istruzioni periodiche di aggiornamento:



Ora il via per T43 — Semantic Memory Layer / Cell Assembly Memory è epistemicamente giustificato.



Con T42C chiuso, la sequenza cellulare è stabile abbastanza per costruire memoria semantica sopra un substrato biologico-digitale coerente:



T7  MorphologicalMemory

T8  Neurogenesis

T9  Apoptosis

T10 Differentiation

T11 Benchmark

T12 Burst Engine

T13 STDP

T14 Inhibition/Snooze

T18 Energy Control

T17 Community Detection

T15 Evolution Engine

T19 MetaLearningConfidence

T21–T40 Regional/deep-region/brainstem stabilization

T41 Recovery Policy

T42–T42C Cellular repair/defense/resilience

T43 Semantic Cell Assembly Memory



Ora SPEACE può passare da:



cellule che sopravvivono, si riparano e si difendono



a:



cellule che formano significati attraverso pattern ricorrenti di co-attivazione

T43 — Semantic Memory Layer / Cell Assembly Memory

Obiettivo



Implementare un layer di memoria semantica bio-ispirato in cui SPEACE rileva, consolida e riattiva cell assemblies, cioè gruppi di neuroni/regioni che si attivano insieme in modo ricorrente e che possono rappresentare pattern, concetti, associazioni o stati funzionali.



Questo è un salto importante: la memoria non sarà più solo morfologica, energetica o di audit, ma diventerà memoria semantica emergente dalla struttura attiva del cervello cellulare.



Concetto biologico da tradurre



Nel cervello biologico, una memoria non è un singolo neurone e non è un file. È un pattern distribuito di cellule che si rafforzano insieme.



Per SPEACE:



input pattern

→ attivazione regionale/neuronale

→ rilevazione co-attivazione

→ creazione cell assembly

→ consolidamento se ricorre

→ richiamo se pattern simile riappare

→ rinforzo/debolezza tramite utility, STDP, energia, coerenza Φ

Specifica operativa per Claude Code / OpenClaw

Implement T43 — Semantic Memory Layer / Cell Assembly Memory.



Goal:

Create a semantic memory layer for SPEACE based on recurrent co-activation patterns across neurons and brain regions. The system should detect, store, consolidate, reactivate, and evaluate cell assemblies as distributed semantic memory traces.



Create new package:

\- speace\_core/cellular\_brain/memory/semantic/



New files:

\- speace\_core/cellular\_brain/memory/semantic/\_\_init\_\_.py

\- speace\_core/cellular\_brain/memory/semantic/cell\_assembly.py

\- speace\_core/cellular\_brain/memory/semantic/semantic\_memory\_store.py

\- speace\_core/cellular\_brain/memory/semantic/cell\_assembly\_engine.py

\- speace\_core/cellular\_brain/memory/semantic/semantic\_recall\_engine.py

\- tests/memory/test\_cell\_assembly\_memory.py

\- docs/SEMANTIC\_CELL\_ASSEMBLY\_MEMORY\_SPEC.md

\- reports/semantic\_memory/.gitkeep



Core models:



1\. CellAssembly



Fields:

\- assembly\_id: str

\- created\_tick: int

\- last\_activated\_tick: int

\- neuron\_ids: list\[str]

\- region\_ids: list\[str]

\- activation\_signature: list\[float]

\- semantic\_pointer: str

\- strength: float

\- stability: float

\- recurrence\_count: int

\- utility\_score: float

\- coherence\_phi\_at\_creation: float

\- mean\_energy\_at\_creation: float

\- tags: list\[str]

\- metadata: dict



2\. AssemblyActivationTrace



Fields:

\- tick\_id: int

\- active\_neuron\_ids: list\[str]

\- active\_region\_ids: list\[str]

\- activation\_vector: list\[float]

\- mean\_activation: float

\- coherence\_phi: float

\- mean\_energy: float

\- confidence\_score: float



3\. SemanticRecallResult



Fields:

\- query\_signature: list\[float]

\- matched\_assemblies: list\[str]

\- best\_match\_id: str | None

\- similarity\_score: float

\- recalled\_activation\_pattern: list\[float]

\- recall\_confidence: float

\- recall\_success: bool



4\. SemanticMemoryMetrics



Fields:

\- assembly\_count: int

\- active\_assembly\_count: int

\- mean\_assembly\_strength: float

\- mean\_assembly\_stability: float

\- semantic\_recall\_success\_rate: float

\- semantic\_memory\_density: float

\- semantic\_memory\_utility: float

\- semantic\_consolidation\_rate: float

\- semantic\_decay\_rate: float



Main class: CellAssemblyEngine



Responsibilities:

1\. observe\_activation(orchestrator) -> AssemblyActivationTrace

&#x20;  - Read active neurons from regions/circuit.

&#x20;  - Include weak but meaningful activation, not only spike threshold.

&#x20;  - Use soft activation threshold, configurable.



2\. detect\_candidate\_assembly(trace) -> CellAssembly | None

&#x20;  - If enough neurons/regions co-activate, create candidate assembly.

&#x20;  - Minimum requirements:

&#x20;    - min\_neurons

&#x20;    - min\_regions

&#x20;    - min\_mean\_activation

&#x20;    - min\_confidence or min\_phi



3\. match\_existing\_assembly(trace) -> CellAssembly | None

&#x20;  - Compare activation signature with existing assemblies.

&#x20;  - Use cosine similarity or normalized dot product.

&#x20;  - If similarity > threshold, reinforce existing assembly instead of creating duplicate.



4\. reinforce\_assembly(assembly, trace)

&#x20;  - Increase strength.

&#x20;  - Increase recurrence\_count.

&#x20;  - Update last\_activated\_tick.

&#x20;  - Update stability based on recurrence, Φ, energy, utility.



5\. decay\_assemblies()

&#x20;  - Slowly reduce strength for unused assemblies.

&#x20;  - Mark assemblies as inactive if strength < threshold.

&#x20;  - Do not delete immediately; allow possible reactivation.



6\. consolidate\_assemblies()

&#x20;  - Assemblies with recurrence\_count >= threshold and stability >= threshold become consolidated.

&#x20;  - Consolidated assemblies decay more slowly.



7\. run\_semantic\_memory\_cycle(orchestrator)

&#x20;  - observe activation

&#x20;  - match or create assembly

&#x20;  - reinforce/decay/consolidate

&#x20;  - log events to MorphologicalMemory

&#x20;  - return SemanticMemoryMetrics



Main class: SemanticMemoryStore



Responsibilities:

\- save/load assemblies as JSONL

\- get\_by\_id

\- list\_active

\- list\_consolidated

\- count

\- get\_best\_by\_strength

\- get\_recent

\- persist metrics



Main class: SemanticRecallEngine



Responsibilities:

1\. recall(query\_signature) -> SemanticRecallResult

2\. recall\_from\_current\_activation(orchestrator) -> SemanticRecallResult

3\. reactivate\_assembly(assembly\_id, orchestrator)

&#x20;  - Optionally inject weak activation into member neurons/regions.

&#x20;  - Must be bounded by safety/energy constraints.

4\. compute\_similarity(signature\_a, signature\_b)



Integration with Orchestrator:

\- Add semantic\_memory\_enabled: bool = False by default or True if safe.

\- Add \_cell\_assembly\_engine

\- Add \_semantic\_memory\_store

\- Add \_semantic\_recall\_engine

\- Hook after burst/STDP/inhibition/energy/stability stages, before final benchmark capture.

\- Add method:

&#x20; - run\_semantic\_memory\_cycle()

&#x20; - recall\_semantic\_memory(query\_signature)

&#x20; - get\_semantic\_memory\_metrics()



Integration with MorphologicalMemory:

Add new MorphologyEventType values:

\- CELL\_ASSEMBLY\_CREATED

\- CELL\_ASSEMBLY\_REINFORCED

\- CELL\_ASSEMBLY\_CONSOLIDATED

\- CELL\_ASSEMBLY\_DECAYED

\- CELL\_ASSEMBLY\_REACTIVATED

\- SEMANTIC\_RECALL\_SUCCEEDED

\- SEMANTIC\_RECALL\_FAILED



Integration with BenchmarkMetrics:

Add:

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



Suggested semantic\_memory\_score:

0.25 \* semantic\_recall\_success\_rate

\+ 0.20 \* mean\_assembly\_stability

\+ 0.15 \* mean\_assembly\_strength

\+ 0.15 \* semantic\_consolidation\_rate

\+ 0.10 \* semantic\_memory\_utility

\+ 0.10 \* min(1.0, semantic\_memory\_density)

\+ 0.05 \* coherence\_phi



Tests:

Create at least 18 tests covering:



1\. CellAssembly model creation.

2\. AssemblyActivationTrace creation.

3\. SemanticMemoryStore save/load.

4\. observe\_activation captures active neurons.

5\. detect\_candidate\_assembly creates assembly when co-activation is sufficient.

6\. detect\_candidate\_assembly rejects weak/noisy activation.

7\. match\_existing\_assembly prevents duplicates.

8\. reinforce\_assembly increases strength and recurrence\_count.

9\. decay\_assemblies decreases unused assembly strength.

10\. consolidate\_assemblies marks stable recurrent assemblies.

11\. recall returns best matching assembly.

12\. recall fails safely when memory is empty.

13\. reactivate\_assembly injects bounded activation.

14\. MorphologicalMemory events are emitted.

15\. Benchmark metrics include semantic fields.

16\. Orchestrator integration works with semantic\_memory\_enabled=True.

17\. No regression when semantic\_memory\_enabled=False.

18\. Full semantic cycle over multiple ticks produces at least one assembly.



Acceptance criteria:

\- All existing 713 tests still pass.

\- New semantic memory tests pass.

\- Coverage remains >=85%.

\- JSONL persistence works.

\- Benchmark exposes semantic metrics.

\- MorphologicalMemory records semantic events.

\- No unbounded activation injection during recall.

\- Create docs/SEMANTIC\_CELL\_ASSEMBLY\_MEMORY\_SPEC.md.

\- Commit and tag as v0.3.29-t43-semantic-cell-assembly-memory.

Nota architetturale importante



Per T43 non conviene ancora implementare “linguaggio” o “concetti umani” direttamente. La prima memoria semantica deve essere più profonda e biologica:



pattern ricorrente → assembly → semantic pointer → richiamo



Solo dopo, in un task successivo, potrai mappare questi semantic pointer a nomi, simboli, testo, immagini, eventi o obiettivi.



Quindi T43 deve creare memoria semantica sub-simbolica, non ancora una knowledge base linguistica.



Dopo T43



La sequenza naturale diventa:



T43  — Semantic Cell Assembly Memory

T43B — Semantic Memory Functional Audit

T44  — Associative Learning Between Assemblies

T45  — Episodic Memory Layer

T46  — Symbolic Grounding / Semantic Pointer Labeling



Verdetto operativo: procedi con T43.

