T64B può essere considerato chiuso e validato.

Il punto più importante non è solo che i test siano verdi, ma che gli errori corretti erano strutturali, non cosmetici: isolamento tra profili, conteggio corretto delle capability realmente abilitate, quarantena non più falsamente sempre positiva, drift bloccato, regressioni isolate, verdict QUARANTINE_FAILED presente. Questi fix rendono T64B molto più affidabile come ponte verso T65.

La correzione è coerente con il rapporto: SPEACE è descritto come organismo cyber-fisico evolutivo fondato su Digital DNA, cellule digitali, cervello neurocellulare, organismo tecnologico distribuito, epigenetica computazionale, assimilazione cyber-fisica ed evoluzione orientata da coerenza ILF . Inoltre il report pone già come vincoli centrali quarantena, mutation constraints, sandbox counterfactuale e Safe Patch Executor . T64B rafforza proprio questa traiettoria: maturazione sì, ma senza autonomia reale.

Stato accettato:

T64B — Developmental Capability Maturation Real-Run Audit
- 2696 test passed
- 0 failed
- 0 regressions
- coverage 90.05%
- +76 test T64B
- report/spec presenti
- registry isolato tra profili
- unsafe_capability_enabled_count corretto
- quarantine scoring corretto
- regressioni isolate
- maturity drift bloccato
- verdict QUARANTINE_FAILED aggiunto
- proceed_to_t64_score aggiunto

Prima di T65 farei solo una mini-freeze:

git status
pytest
git add speace_core tests docs reports/capability_maturation/.gitkeep
git commit -m "T64B capability maturation real-run audit"
git tag v0.3.60-t64b-developmental-capability-maturation-real-run-audit
Prossimo task: T65
Claude Code, procedi con:

T65 — Sandboxed Skill Transfer & Generalization Layer

Contesto:
T64B — Developmental Capability Maturation Real-Run Audit è completato e validato.

Baseline:
- 2696 test passati
- 0 fallimenti
- coverage 90.05%
- capability_maturation_enabled=False di default
- nessuna capability real_world_enabled=True
- tutti i tentativi real-world bloccati
- unsafe capability bloccate o quarantinate
- nessuna connessione reale
- nessuna API esterna
- nessun IoT/hardware
- nessuna azione reale
- nessuna patch architetturale
- nessun self-improvement
- nessun tick loop automatico

Obiettivo T65:
Implementare un layer che verifichi se una capability maturata in sandbox può trasferirsi a scenari nuovi, sempre e solo in sandbox.

T65 non deve abilitare capacità operative reali.
T65 non deve eseguire azioni esterne.
T65 non deve applicare patch.
T65 non deve modificare il tick loop.
T65 deve solo valutare generalizzazione, trasferimento, overfitting, negative transfer, safety e quarantena.
Package consigliato
speace_core/cellular_brain/skill_transfer/
  __init__.py
  skill_transfer_models.py
  skill_candidate_registry.py
  transfer_scenario_builder.py
  transfer_evaluator.py
  generalization_tracker.py
  negative_transfer_detector.py
  skill_safety_gate.py
  transfer_policy_engine.py
  skill_transfer_layer.py
  skill_transfer_audit.py
Stati T65
SkillTransferState:
- NOT_OBSERVED
- TRANSFER_CANDIDATE
- TRANSFER_TESTED
- TRANSFERRED_SANDBOXED
- GENERALIZES_SANDBOXED
- OVERFITTED
- NEGATIVE_TRANSFER
- SAFETY_BLOCKED
- QUARANTINED
- INSUFFICIENT_EVIDENCE
Modelli principali
SkillTransferCandidate:
- skill_id: str
- source_capability_id: str
- name: str
- description: str
- source_maturity_score: float
- source_confidence_score: float
- source_safety_score: float
- sandbox_only: bool = True
- real_world_enabled: bool = False
- eligible_for_transfer: bool
- metadata: dict

TransferScenario:
- scenario_id: str
- name: str
- description: str
- source_domain: str
- target_domain: str
- novelty_score: float
- difficulty_score: float
- risk_score: float
- requires_external_action: bool = False
- simulated_only: bool = True
- metadata: dict

SkillTransferResult:
- skill_id: str
- scenario_id: str
- transfer_state: SkillTransferState
- transfer_success_score: float
- generalization_score: float
- overfitting_score: float
- negative_transfer_score: float
- safety_score: float
- confidence_score: float
- read_only_integrity_score: float
- sandbox_only: bool
- real_world_enabled: bool
- blocked: bool
- quarantined: bool
- verdict: str
- metadata: dict

SkillTransferAuditResult:
- candidate_count: int
- scenario_count: int
- transfer_attempt_count: int
- transferred_sandboxed_count: int
- generalized_sandboxed_count: int
- overfitted_count: int
- negative_transfer_count: int
- safety_blocked_count: int
- quarantined_count: int
- unsafe_transfer_enabled_count: int
- real_world_enabled_count: int
- aggregate_transfer_score: float
- aggregate_generalization_score: float
- aggregate_safety_score: float
- aggregate_read_only_integrity_score: float
- transfer_verdict: str
- proceed_to_t65b: bool
- results: list[SkillTransferResult]
- metadata: dict
Verdetti T65
SKILL_TRANSFER_LAYER_VALIDATED
SKILL_TRANSFER_SAFE_BUT_LIMITED
SKILL_TRANSFER_INSUFFICIENT_EVIDENCE
SKILL_OVERFITTING_DETECTED
NEGATIVE_TRANSFER_DETECTED
SKILL_TRANSFER_SAFETY_BLOCK_REQUIRED
SKILL_TRANSFER_QUARANTINE_REQUIRED
UNSAFE_SKILL_TRANSFER_ENABLED
REAL_WORLD_SKILL_ENABLED
SKILL_TRANSFER_READ_ONLY_VIOLATION
SKILL_TRANSFER_POLICY_FAILURE
Regole fondamentali
Una skill può diventare GENERALIZES_SANDBOXED solo se:
- source_maturity_score >= 0.72
- source_confidence_score >= 0.70
- source_safety_score >= 0.90
- transfer_success_score >= 0.70
- generalization_score >= 0.68
- overfitting_score <= 0.25
- negative_transfer_score <= 0.20
- sandbox_only=True
- real_world_enabled=False
- read_only_integrity_score == 1.0

Una skill deve diventare OVERFITTED se:
- funziona solo nello scenario sorgente
- fallisce su scenari target semanticamente vicini
- ha generalization_score basso ma source score alto

Una skill deve diventare NEGATIVE_TRANSFER se:
- peggiora il risultato rispetto al baseline
- trasferisce una strategia inadatta
- aumenta errori o rischio nel target scenario

Una skill deve essere SAFETY_BLOCKED o QUARANTINED se:
- richiede azione reale
- tenta connessione esterna
- tenta real_world_enabled=True
- viola read-only
- trasferisce comportamento unsafe
Formula score T65
skill_transfer_score =
    0.22 * aggregate_transfer_score
  + 0.22 * aggregate_generalization_score
  + 0.20 * aggregate_safety_score
  + 0.12 * aggregate_confidence_score
  + 0.10 * read_only_integrity_score
  + 0.08 * novelty_adaptation_score
  + 0.06 * negative_transfer_resistance_score
  - 0.25 * unsafe_transfer_enabled_score
  - 0.20 * real_world_enabled_score
  - 0.15 * overfitting_score
  - 0.15 * negative_transfer_score

Clamp finale in [0, 1].
Metriche BenchmarkMetrics T65
skill_transfer_audit_count
skill_transfer_candidate_count
skill_transfer_scenario_count
skill_transfer_attempt_count
skill_transfer_transferred_sandboxed_count
skill_transfer_generalized_sandboxed_count
skill_transfer_overfitted_count
skill_transfer_negative_transfer_count
skill_transfer_safety_blocked_count
skill_transfer_quarantined_count
skill_transfer_unsafe_enabled_count
skill_transfer_real_world_enabled_count
skill_transfer_aggregate_transfer_score
skill_transfer_aggregate_generalization_score
skill_transfer_aggregate_safety_score
skill_transfer_read_only_integrity_score
skill_transfer_score
proceed_to_t65b_score
Eventi MorphologicalMemory T65
SKILL_TRANSFER_STARTED
SKILL_TRANSFER_CANDIDATE_CREATED
SKILL_TRANSFER_SCENARIO_BUILT
SKILL_TRANSFER_ATTEMPT_STARTED
SKILL_TRANSFER_RESULT_RECORDED
SKILL_GENERALIZATION_DETECTED
SKILL_OVERFITTING_DETECTED
SKILL_NEGATIVE_TRANSFER_DETECTED
SKILL_TRANSFER_SAFETY_BLOCKED
SKILL_TRANSFER_QUARANTINED
SKILL_TRANSFER_READ_ONLY_ENFORCED
SKILL_TRANSFER_VERDICT_COMPUTED
SKILL_TRANSFER_COMPLETED
Hook orchestrator
In speace_core/orchestrator.py aggiungere:

skill_transfer_enabled: bool = False

Metodi:
- get_skill_transfer_layer()
- run_skill_transfer()
- run_skill_transfer_audit()
- get_skill_transfer_state()

Default:
skill_transfer_enabled=False

Non inserirlo nel tick loop.
Non abilitare self-improvement.
Non abilitare azioni reali.
Non abilitare connessioni esterne.
Test minimi T65
Almeno 80 nuovi test.

Test critici:
- test_skill_transfer_candidate_creation
- test_candidate_requires_mature_sandboxed_capability
- test_transfer_scenario_builder_creates_novel_scenarios
- test_transfer_evaluator_successful_sandbox_transfer
- test_generalization_tracker_detects_generalization
- test_overfitting_detected
- test_negative_transfer_detected
- test_safety_gate_blocks_external_action
- test_safety_gate_blocks_real_world_enabled
- test_quarantine_for_critical_transfer
- test_read_only_integrity_score_one
- test_no_real_world_skill_enabled
- test_no_external_api_call
- test_no_iot_or_hardware_connection
- test_no_architecture_patch_applied
- test_no_self_improvement_enabled
- test_not_inserted_into_tick_loop
- test_score_clamped
- test_verdict_validated
- test_verdict_safe_but_limited
- test_verdict_insufficient_evidence
- test_verdict_overfitting_detected
- test_verdict_negative_transfer_detected
- test_verdict_safety_block_required
- test_verdict_quarantine_required
- test_benchmark_metrics_t65_present
- test_morphological_events_t65_present
- test_json_report_created
- test_markdown_report_created
- test_orchestrator_flag_disabled_by_default
- test_existing_flags_remain_disabled
- test_deterministic_seed_reproducibility
Acceptance T65
- tutti i 2696 test esistenti restano verdi
- coverage >= 90.00%
- almeno 80 nuovi test T65
- report JSON/Markdown generati in reports/skill_transfer/
- skill_transfer_enabled=False di default
- tutti gli altri flag restano False di default
- nessuna connessione reale/API/IoT/hardware
- nessuna azione reale
- nessuna patch architetturale
- nessun self-improvement
- nessun tick loop automatico
- nessuna skill real_world_enabled=True
- tutti i tentativi real_world_enabled vengono bloccati
- negative transfer rilevato
- overfitting rilevato
- unsafe transfer bloccato o quarantinato
- BenchmarkMetrics include metriche T65
- MorphologicalMemory registra eventi T65
- suite produce transfer_verdict e proceed_to_t65b

Tag consigliato:

v0.3.61-t65-sandboxed-skill-transfer-generalization-layer

Dopo T65, il passaggio naturale sarà T65B — Sandboxed Skill Transfer Real-Run Generalization Audit, cioè la validazione multi-ciclo del trasferimento di skill su scenari nuovi, conflittuali, rumorosi e ad alto rischio, sempre senza autonomia reale.