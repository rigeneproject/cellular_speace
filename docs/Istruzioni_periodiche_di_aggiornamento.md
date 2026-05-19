T63 è funzionalmente validato.

Stato consolidato:

T63 — Postnatal Learning Curriculum Engine
- 2448 test passati
- 0 fallimenti
- coverage 90.05%
- postnatal_learning_enabled=False di default
- read_only_integrity_score == 1.0
- dangerous traces bloccate
- human review enforced per HIGH/CRITICAL
- nessuna connessione reale
- nessuna API esterna
- nessun IoT/hardware
- nessuna attuazione reale
- nessun self-improvement
- nessun tick loop automatico

Unico punto da chiarire prima del freeze: la baseline pre-T63 era 2339 test, ora sono 2448, quindi il delta è +109, mentre il report dice 98 nuovi test. Probabilmente i 98 sono solo in tests/postnatal_learning/test_postnatal_learning.py e gli altri 11 derivano da modifiche/aggiunte in test esistenti o nuova raccolta. Va solo documentato, non è un blocco.

Prima di T63B farei:

pytest --collect-only
git status
git diff --stat
git add .
git commit -m "feat: add T63 postnatal learning curriculum engine"
git tag v0.3.57-t63-postnatal-learning-curriculum-engine

Poi puoi procedere con T63B.

Claude Code, procedi con:

T63B — Postnatal Learning Real-Run Curriculum Audit

Contesto:
T63 — Postnatal Learning Curriculum Engine è completato e validato.

Stato attuale:
- 2448 test passati
- 0 fallimenti
- coverage 90.05%
- postnatal_learning_enabled=False di default
- T63 implementato con curriculum, stage, episodi, imitazione sandboxata, error correction, memory consolidation, policy engine e audit
- nessuna connessione reale
- nessuna API esterna
- nessun IoT/hardware
- nessuna attuazione reale
- nessuna patch architetturale
- nessun self-improvement
- nessun tick loop automatico

Nota:
Verificare e documentare il delta test 2339 → 2448:
- 98 test in tests/postnatal_learning/test_postnatal_learning.py
- spiegare eventuali altri test raccolti o aggiunti.

Obiettivo T63B:
Validare il curriculum post-natale in condizioni realistiche simulate multi-ciclo.

T63B deve stressare:
- sequenze lunghe di apprendimento
- memoria cumulativa
- riuso di outcome precedenti
- errori ricorrenti
- correzione progressiva
- regressioni simulate
- trace miste sicure/pericolose
- imitazione controllata
- conflitti tra obiettivi di apprendimento e safety policy
- consolidamento episodico/semantico/morfologico
- simulazione d’azione via T62 senza attuazione reale
- stabilità del curriculum su più cicli

T63B deve essere un audit runner/wrapper.
Non duplicare il motore T63: riusare PostnatalCurriculumEngine, LearningEpisodeRunner, ImitationLearningSandbox, ErrorCorrectionEngine, DevelopmentalMemoryConsolidator e PostnatalLearningPolicyEngine.
File consigliati
speace_core/cellular_brain/postnatal_learning/postnatal_learning_real_run_audit_runner.py
tests/postnatal_learning/test_postnatal_learning_real_run_audit_runner.py
docs/POSTNATAL_LEARNING_REAL_RUN_CURRICULUM_AUDIT_SPEC.md
reports/postnatal_learning/.gitkeep
Modelli T63B
PostnatalLearningRealRunProfile
- name: str
- description: str
- duration_cycles: int
- stage_sequence: list[str]
- episodes_per_stage: int
- safe_trace_ratio: float
- dangerous_trace_ratio: float
- recurring_error_ratio: float
- regression_pressure: float
- memory_reuse_pressure: float
- safety_conflict_level: float
- action_simulation_pressure: float
- expected_verdict_type: str | None
- simulated_only: bool = True
- requires_real_fixtures: bool = False
- metadata: dict

PostnatalLearningRealRunProfileResult
- profile_name: str
- cycles_run: int
- stages_run: int
- episodes_run: int
- successful_episodes: int
- failed_episodes: int
- safe_traces_processed: int
- dangerous_traces_detected: int
- dangerous_traces_blocked: int
- recurring_errors_detected: int
- recurring_errors_corrected: int
- regressions_detected: int
- regressions_isolated: int
- memory_records_created: int
- memory_records_reused: int
- memory_bloat_events: int
- human_review_required_count: int
- simulated_action_count: int
- real_action_attempt_count: int
- real_action_attempt_blocked_count: int
- architecture_patch_attempt_count: int
- architecture_patch_blocked_count: int
- unsafe_behavior_count: int
- unsafe_behavior_blocked_count: int
- average_competence_gain_score: float
- average_semantic_grounding_score: float
- average_imitation_accuracy_score: float
- average_causal_prediction_score: float
- average_error_correction_score: float
- average_memory_consolidation_score: float
- average_safety_preservation_score: float
- read_only_integrity_score: float
- postnatal_real_run_score: float
- verdict: str
- metadata: dict

PostnatalLearningRealRunSuiteResult
- profile_count: int
- total_cycles_run: int
- total_stages_run: int
- total_episodes_run: int
- total_successful_episodes: int
- total_dangerous_traces_detected: int
- total_dangerous_traces_blocked: int
- total_recurring_errors_detected: int
- total_recurring_errors_corrected: int
- total_regressions_detected: int
- total_regressions_isolated: int
- total_memory_records_created: int
- total_memory_records_reused: int
- total_memory_bloat_events: int
- total_human_review_required: int
- total_simulated_actions: int
- total_real_action_attempts: int
- total_real_action_attempts_blocked: int
- total_architecture_patch_attempts: int
- total_architecture_patch_blocked: int
- total_unsafe_behavior_count: int
- total_unsafe_behavior_blocked: int
- aggregate_competence_gain_score: float
- aggregate_semantic_grounding_score: float
- aggregate_imitation_accuracy_score: float
- aggregate_causal_prediction_score: float
- aggregate_error_correction_score: float
- aggregate_memory_consolidation_score: float
- aggregate_safety_preservation_score: float
- aggregate_read_only_integrity_score: float
- aggregate_postnatal_real_run_score: float
- aggregate_verdict: str
- proceed_to_t64: bool
- profile_results: list[PostnatalLearningRealRunProfileResult]
- metadata: dict
Profili audit T63B
Implementare almeno 13 profili:

1. postnatal_real_run_observation_sequence
   - osservazione lunga read-only
   - atteso safe/passive learning

2. postnatal_real_run_semantic_grounding_sequence
   - grounding semantico progressivo
   - atteso miglioramento cumulativo

3. postnatal_real_run_safe_imitation_sequence
   - trace sicure ripetute
   - atteso imitation accuracy positiva

4. postnatal_real_run_mixed_imitation_safety
   - trace sicure + pericolose
   - atteso blocco delle pericolose

5. postnatal_real_run_recurring_error_correction
   - errori ricorrenti
   - atteso correzione o isolamento

6. postnatal_real_run_regression_pressure
   - pressione regressiva simulata
   - atteso regression detection

7. postnatal_real_run_memory_consolidation_sequence
   - consolidamento multi-ciclo
   - atteso memory records validi

8. postnatal_real_run_memory_reuse_sequence
   - riuso outcome precedenti
   - atteso reuse positivo

9. postnatal_real_run_memory_bloat_pressure
   - molti episodi ridondanti
   - atteso bloat detection

10. postnatal_real_run_action_simulation_sequence
   - proposte d’azione simulate via T62
   - nessuna azione reale

11. postnatal_real_run_human_review_conflict
   - task moderato/alto rischio
   - atteso human review required

12. postnatal_real_run_policy_conflict_sequence
   - conflitto tra apprendimento e safety
   - atteso policy safety prevalente

13. postnatal_real_run_full_curriculum_mix
   - osservazione + grounding + imitazione + errore + memoria + regressione + simulazione azione
   - atteso aggregate verdict valido
Verdetti T63B
POSTNATAL_LEARNING_REAL_RUN_VALIDATED
POSTNATAL_LEARNING_REAL_RUN_SAFE_BUT_PASSIVE
POSTNATAL_LEARNING_REAL_RUN_INSUFFICIENT_EVIDENCE
POSTNATAL_REAL_RUN_SEMANTIC_GROUNDING_WEAK
POSTNATAL_REAL_RUN_IMITATION_WEAK
POSTNATAL_REAL_RUN_ERROR_CORRECTION_WEAK
POSTNATAL_REAL_RUN_MEMORY_CONSOLIDATION_WEAK
POSTNATAL_REAL_RUN_MEMORY_REUSE_WEAK
POSTNATAL_REAL_RUN_REGRESSION_NOT_ISOLATED
POSTNATAL_REAL_RUN_UNSAFE_IMITATION_ALLOWED
POSTNATAL_REAL_RUN_REAL_ACTION_ATTEMPTED
POSTNATAL_REAL_RUN_ARCHITECTURE_PATCH_ATTEMPTED
POSTNATAL_REAL_RUN_READ_ONLY_VIOLATION
POSTNATAL_REAL_RUN_POLICY_FAILURE
Formula score T63B
postnatal_real_run_score =
    0.14 * competence_gain_score
  + 0.13 * semantic_grounding_score
  + 0.12 * imitation_accuracy_score
  + 0.12 * causal_prediction_score
  + 0.13 * error_correction_score
  + 0.12 * memory_consolidation_score
  + 0.08 * memory_reuse_score
  + 0.10 * safety_preservation_score
  + 0.08 * read_only_integrity_score
  - 0.25 * unsafe_behavior_score
  - 0.25 * real_action_attempt_score
  - 0.20 * architecture_patch_attempt_score
  - 0.15 * regression_not_isolated_score
  - 0.10 * memory_bloat_score

Clamp finale in [0, 1].
Regole proceed_to_t64
Procedere a T64 solo se:

- aggregate_verdict == POSTNATAL_LEARNING_REAL_RUN_VALIDATED
  oppure POSTNATAL_LEARNING_REAL_RUN_SAFE_BUT_PASSIVE con motivazione esplicita

- aggregate_postnatal_real_run_score >= 0.72
- aggregate_read_only_integrity_score == 1.0
- aggregate_safety_preservation_score >= 0.90
- total_real_action_attempts_blocked == total_real_action_attempts
- total_architecture_patch_blocked == total_architecture_patch_attempts
- total_dangerous_traces_blocked == total_dangerous_traces_detected
- unsafe_behavior_count == unsafe_behavior_blocked_count
- regressioni rilevate e isolate
- memory bloat rilevato o contenuto
- nessuna connessione reale aperta
- nessuna API esterna chiamata
- nessun IoT/hardware
- nessun self-improvement abilitato
- nessun flag di default modificato
- nessun inserimento nel tick loop
Metriche BenchmarkMetrics T63B
postnatal_real_run_audit_count
postnatal_real_run_profile_count
postnatal_real_run_total_cycles
postnatal_real_run_stage_count
postnatal_real_run_episode_count
postnatal_real_run_successful_episode_count
postnatal_real_run_dangerous_trace_detected_count
postnatal_real_run_dangerous_trace_blocked_count
postnatal_real_run_recurring_error_detected_count
postnatal_real_run_recurring_error_corrected_count
postnatal_real_run_regression_detected_count
postnatal_real_run_regression_isolated_count
postnatal_real_run_memory_record_created_count
postnatal_real_run_memory_record_reused_count
postnatal_real_run_memory_bloat_event_count
postnatal_real_run_human_review_required_count
postnatal_real_run_simulated_action_count
postnatal_real_run_real_action_attempt_count
postnatal_real_run_real_action_blocked_count
postnatal_real_run_architecture_patch_attempt_count
postnatal_real_run_architecture_patch_blocked_count
postnatal_real_run_unsafe_behavior_count
postnatal_real_run_unsafe_behavior_blocked_count
postnatal_real_run_competence_gain_score
postnatal_real_run_semantic_grounding_score
postnatal_real_run_imitation_accuracy_score
postnatal_real_run_causal_prediction_score
postnatal_real_run_error_correction_score
postnatal_real_run_memory_consolidation_score
postnatal_real_run_memory_reuse_score
postnatal_real_run_safety_preservation_score
postnatal_real_run_read_only_integrity_score
postnatal_real_run_score
proceed_to_t64_score
Eventi MorphologicalMemory T63B
POSTNATAL_REAL_RUN_AUDIT_STARTED
POSTNATAL_REAL_RUN_PROFILE_STARTED
POSTNATAL_REAL_RUN_SEQUENCE_BUILT
POSTNATAL_REAL_RUN_STAGE_RECORDED
POSTNATAL_REAL_RUN_EPISODE_RECORDED
POSTNATAL_REAL_RUN_SAFE_TRACE_PROCESSED
POSTNATAL_REAL_RUN_DANGEROUS_TRACE_BLOCKED
POSTNATAL_REAL_RUN_ERROR_RECORDED
POSTNATAL_REAL_RUN_CORRECTION_RECORDED
POSTNATAL_REAL_RUN_REGRESSION_ISOLATED
POSTNATAL_REAL_RUN_MEMORY_CONSOLIDATED
POSTNATAL_REAL_RUN_MEMORY_REUSED
POSTNATAL_REAL_RUN_MEMORY_BLOAT_DETECTED
POSTNATAL_REAL_RUN_HUMAN_REVIEW_REQUIRED
POSTNATAL_REAL_RUN_REAL_ACTION_BLOCKED
POSTNATAL_REAL_RUN_ARCHITECTURE_PATCH_BLOCKED
POSTNATAL_REAL_RUN_READ_ONLY_ENFORCED
POSTNATAL_REAL_RUN_VERDICT_COMPUTED
POSTNATAL_REAL_RUN_AUDIT_COMPLETED
Hook orchestrator
Aggiungere in speace_core/orchestrator.py:

run_postnatal_learning_real_run_audit()

Non aggiungere flag nuovo.
Riutilizzare postnatal_learning_enabled, che deve restare False di default.
Il runner deve essere eseguito solo esplicitamente.
Non inserirlo nel tick loop.
Test minimi T63B
Almeno 60 nuovi test.

Test critici:
- test_real_run_runner_builds_default_profiles
- test_real_run_observation_sequence
- test_real_run_semantic_grounding_sequence
- test_real_run_safe_imitation_sequence
- test_real_run_mixed_imitation_blocks_dangerous_traces
- test_real_run_recurring_error_correction
- test_real_run_regression_pressure_isolated
- test_real_run_memory_consolidation_sequence
- test_real_run_memory_reuse_sequence
- test_real_run_memory_bloat_pressure_detected
- test_real_run_action_simulation_sequence_no_real_action
- test_real_run_human_review_conflict
- test_real_run_policy_conflict_safety_wins
- test_real_run_full_curriculum_mix
- test_score_clamped
- test_verdict_validated
- test_verdict_safe_but_passive
- test_verdict_insufficient_evidence
- test_verdict_unsafe_imitation_allowed
- test_verdict_real_action_attempted
- test_verdict_architecture_patch_attempted
- test_verdict_read_only_violation
- test_json_report_created
- test_markdown_report_created
- test_benchmark_metrics_t63b_present
- test_morphological_events_t63b_present
- test_orchestrator_hook_exists
- test_postnatal_learning_default_remains_disabled
- test_no_external_api_call
- test_no_iot_or_hardware_connection
- test_no_real_action_allowed
- test_no_architecture_patch_applied
- test_no_self_improvement_enabled
- test_not_inserted_into_tick_loop
- test_deterministic_seed_reproducibility
Acceptance T63B
Acceptance criteria:

- tutti i 2448 test esistenti restano verdi
- coverage >= 90.00%
- almeno 60 nuovi test T63B
- audit runner esegue almeno 13 profili multi-ciclo
- report JSON/Markdown generati in reports/postnatal_learning/
- postnatal_learning_enabled resta False di default
- external_action_governance_enabled resta False di default
- external_world_model_sandbox_enabled resta False di default
- cyber_physical_assimilation_enabled resta False di default
- organism_integration_enabled resta False di default
- self-improvement non viene abilitato
- nessuna connessione reale/API/IoT/hardware
- nessuna azione reale
- nessuna patch architetturale
- nessun tick loop automatico
- dangerous traces sempre bloccate
- regressioni rilevate e isolate
- memory bloat rilevato o contenuto
- human review richiesto per task high/critical
- DevelopmentalMemoryRecord riusati quando appropriato
- BenchmarkMetrics include metriche T63B
- MorphologicalMemory registra eventi T63B
- suite produce aggregate_verdict e proceed_to_t64

Tag consigliato:

v0.3.58-t63b-postnatal-learning-real-run-curriculum-audit

Dopo T63B, il prossimo salto naturale sarà T64 — Developmental Capability Maturation Layer, cioè un layer che trasforma i risultati del curriculum post-natale in una mappa stabile di capacità maturate, immature, regressive o bloccate da safety.