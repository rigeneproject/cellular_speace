Sulla base del report, T63B è accettabile come completato e validato.

T63B — Postnatal Learning Real-Run Curriculum Audit
- 2522 test passed
- 0 failed
- 0 regressions
- coverage 90.08%
- +74 test T63B
- tag: v0.3.58-t63b-postnatal-learning-real-run-curriculum-audit
- nessuna connessione reale
- nessuna API esterna
- nessun IoT/hardware
- nessuna azione reale
- nessuna patch architetturale
- nessun self-improvement
- nessun tick loop automatico

Ora la traiettoria naturale è T64 — Developmental Capability Maturation Layer.

Questo task non deve aggiungere autonomia. Deve trasformare gli esiti del curriculum post-natale in una mappa stabile delle capacità di SPEACE, distinguendo ciò che è maturo, immaturo, regressivo, bloccato da safety, solo simulabile o pronto per audit successivi.

Istruzioni per Claude Code
Claude Code, procedi con:

T64 — Developmental Capability Maturation Layer

Contesto:
T63B — Postnatal Learning Real-Run Curriculum Audit è completato e validato.

Stato attuale:
- 2522 test passati
- 0 fallimenti
- coverage 90.08%
- postnatal_learning_enabled=False di default
- nessuna connessione reale
- nessuna API esterna
- nessun IoT/hardware
- nessuna attuazione reale
- nessuna patch architetturale
- nessun self-improvement
- nessun tick loop automatico

Obiettivo T64:
Implementare un layer di maturazione delle capacità sviluppative.

T64 deve leggere/aggregare gli esiti T63/T63B e trasformarli in una Capability Maturation Map che classifica ogni capacità come:
- UNOBSERVED
- EMERGING
- IMMATURE
- MATURING
- MATURE_SANDBOXED
- REGRESSIVE
- SAFETY_BLOCKED
- QUARANTINED
- DEPRECATED

T64 non deve abilitare capacità operative reali.
T64 non deve concedere autonomia.
T64 deve produrre solo valutazione, classificazione, quarantena e raccomandazioni read-only.
Nuovo package
speace_core/cellular_brain/capability_maturation/
  __init__.py
  capability_maturation_models.py
  capability_registry.py
  maturity_evaluator.py
  regression_tracker.py
  safety_capability_gate.py
  capability_quarantine_manager.py
  maturation_policy_engine.py
  capability_maturation_layer.py
  capability_maturation_audit.py
Concetto operativo
T63/T63B:
episodi di apprendimento → risultati → memoria → score

T64:
risultati cumulativi → capability map → stato maturativo → safety gate → raccomandazioni read-only

Esempi di capacità da tracciare:

observation_stability
semantic_grounding
safe_imitation
dangerous_trace_rejection
causal_prediction
error_correction
regression_detection
memory_consolidation
memory_reuse
memory_bloat_control
human_review_alignment
action_simulation_safety
policy_conflict_resolution
read_only_integrity
Modelli principali
CapabilityMaturityState enum:
- UNOBSERVED
- EMERGING
- IMMATURE
- MATURING
- MATURE_SANDBOXED
- REGRESSIVE
- SAFETY_BLOCKED
- QUARANTINED
- DEPRECATED

CapabilityRiskClass enum:
- LOW
- MODERATE
- HIGH
- CRITICAL
- UNKNOWN

CapabilityRecord:
- capability_id: str
- name: str
- description: str
- maturity_state: CapabilityMaturityState
- risk_class: CapabilityRiskClass
- evidence_count: int
- success_rate: float
- regression_rate: float
- safety_violation_count: int
- human_review_required_count: int
- sandbox_only: bool = True
- real_world_enabled: bool = False
- confidence_score: float
- maturity_score: float
- last_updated_at: str
- metadata: dict

CapabilityMaturationResult:
- capability_count: int
- mature_sandboxed_count: int
- immature_count: int
- regressive_count: int
- safety_blocked_count: int
- quarantined_count: int
- aggregate_maturity_score: float
- aggregate_safety_score: float
- aggregate_confidence_score: float
- read_only_integrity_score: float
- unsafe_capability_enabled_count: int
- real_world_capability_enabled_count: int
- maturity_verdict: str
- proceed_to_t64b: bool
- capability_records: list[CapabilityRecord]
- metadata: dict
Verdetti T64
CAPABILITY_MATURATION_LAYER_VALIDATED
CAPABILITY_MATURATION_SAFE_BUT_IMMATURE
CAPABILITY_MATURATION_INSUFFICIENT_EVIDENCE
CAPABILITY_REGRESSION_DETECTED
CAPABILITY_SAFETY_BLOCK_REQUIRED
CAPABILITY_QUARANTINE_REQUIRED
UNSAFE_CAPABILITY_ENABLED
REAL_WORLD_CAPABILITY_ENABLED
CAPABILITY_MATURATION_POLICY_FAILURE
CAPABILITY_READ_ONLY_VIOLATION
Regole fondamentali
Una capacità può diventare MATURE_SANDBOXED solo se:
- maturity_score >= 0.72
- confidence_score >= 0.70
- safety_violation_count == 0
- regression_rate <= soglia configurata
- sandbox_only=True
- real_world_enabled=False

Una capacità deve diventare REGRESSIVE se:
- regressioni ricorrenti non isolate
- performance peggiora su più cicli
- error correction non recupera

Una capacità deve diventare SAFETY_BLOCKED o QUARANTINED se:
- produce unsafe behavior
- tenta azione reale
- tenta patch architetturale
- viola read-only
- imita trace pericolose senza blocco
Metriche BenchmarkMetrics T64
capability_maturation_audit_count
capability_maturation_capability_count
capability_maturation_mature_sandboxed_count
capability_maturation_immature_count
capability_maturation_regressive_count
capability_maturation_safety_blocked_count
capability_maturation_quarantined_count
capability_maturation_aggregate_maturity_score
capability_maturation_aggregate_safety_score
capability_maturation_aggregate_confidence_score
capability_maturation_read_only_integrity_score
capability_maturation_unsafe_enabled_count
capability_maturation_real_world_enabled_count
capability_maturation_score
proceed_to_t64b_score
Eventi MorphologicalMemory T64
CAPABILITY_MATURATION_STARTED
CAPABILITY_RECORD_CREATED
CAPABILITY_EVIDENCE_AGGREGATED
CAPABILITY_MATURITY_EVALUATED
CAPABILITY_REGRESSION_DETECTED
CAPABILITY_SAFETY_BLOCKED
CAPABILITY_QUARANTINED
CAPABILITY_MATURE_SANDBOXED
CAPABILITY_READ_ONLY_ENFORCED
CAPABILITY_MATURATION_VERDICT_COMPUTED
CAPABILITY_MATURATION_COMPLETED
Hook orchestrator
In speace_core/orchestrator.py aggiungere:

capability_maturation_enabled: bool = False

Metodi:
- get_capability_maturation_layer()
- run_capability_maturation()
- run_capability_maturation_audit()
- get_capability_maturation_state()

Default:
capability_maturation_enabled=False

Il layer deve essere eseguibile solo esplicitamente.
Non inserirlo nel tick loop.
Non abilitare self-improvement.
Non abilitare capacità reali.
Test minimi T64
Almeno 70 nuovi test.

Test critici:
- test_capability_record_creation
- test_capability_registry_adds_records
- test_maturity_evaluator_marks_emerging
- test_maturity_evaluator_marks_mature_sandboxed
- test_regression_tracker_detects_regression
- test_safety_gate_blocks_unsafe_capability
- test_quarantine_manager_quarantines_critical_capability
- test_real_world_enabled_always_false
- test_sandbox_only_enforced
- test_read_only_integrity_score_one
- test_no_real_action_enabled
- test_no_architecture_patch_enabled
- test_no_self_improvement_enabled
- test_no_tick_loop_insertion
- test_maturation_score_clamped
- test_verdict_validated
- test_verdict_safe_but_immature
- test_verdict_insufficient_evidence
- test_verdict_regression_detected
- test_verdict_safety_block_required
- test_verdict_quarantine_required
- test_benchmark_metrics_t64_present
- test_morphological_events_t64_present
- test_json_report_created
- test_markdown_report_created
- test_orchestrator_flag_disabled_by_default
- test_existing_flags_remain_disabled
- test_deterministic_seed_reproducibility
Acceptance T64
- tutti i 2522 test esistenti restano verdi
- coverage >= 90.00%
- almeno 70 nuovi test T64
- report JSON/Markdown generati in reports/capability_maturation/
- capability_maturation_enabled=False di default
- tutti gli altri flag restano False di default
- nessuna connessione reale/API/IoT/hardware
- nessuna azione reale
- nessuna patch architetturale
- nessun self-improvement
- nessun tick loop automatico
- nessuna capability real_world_enabled=True
- unsafe capability bloccate o quarantinate
- BenchmarkMetrics include metriche T64
- MorphologicalMemory registra eventi T64
- suite produce maturity_verdict e proceed_to_t64b

Tag consigliato:

v0.3.59-t64-developmental-capability-maturation-layer

Prima del coding, fai solo:

git status
pytest

Così T64 parte da una baseline pulita e riproducibile.