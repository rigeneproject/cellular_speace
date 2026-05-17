# T42 — Cellular Adaptive Defense & Repair Layer

**Version:** v0.3.26-t42-cellular-adaptive-defense-repair  
**Date:** 2026-05-17  
**Status:** Implemented  
**Depends on:** T41 (Long-Horizon Recovery Consolidation & Policy Freezing)

## 1. Objective

Aggiungere uno strato cellulare di stress, danno, riparazione, difesa e adattamento epigenetico per rendere le cellule digitali "più vive" prima di costruire funzioni cognitive superiori (memoria semantica).

## 2. Problem Statement

Il sistema attuale gestisce plasticità, energia e apoptosi a livello di circuito, ma non ha un modello per-cell di:
- stress fisiologico cumulativo
- danno reversibile/funzionale/strutturale/critico
- riparazione autonoma con budget energetico
- difesa attiva (quarantena, firewall, snooze)
- adattamento epigenetico locale

## 3. Architecture

### 3.1 Components

| File | Role |
|---|---|
| `speace_core/cellular_brain/cells/cellular_stress.py` | Valuta stress per-cell |
| `speace_core/cellular_brain/cells/cellular_damage.py` | Traccia e classifica danno |
| `speace_core/cellular_brain/cells/cellular_repair_engine.py` | Esegue riparazioni |
| `speace_core/cellular_brain/cells/cellular_defense_engine.py` | Attiva difese |
| `speace_core/cellular_brain/cells/cellular_epigenetic_adapter.py` | Adatta espressione genica locale |

### 3.2 Models

| Model | Role |
|---|---|
| `CellularStressState` | Snapshot stress per cell |
| `CellularDamageState` | Snapshot danno per cell |
| `RepairAction` | Azione di riparazione singola |
| `DefenseAction` | Azione di difesa singola |
| `GeneExpressionProfile` | Profilo genico locale |
| `EpigeneticShift` | Record di shift epigenetico |

## 4. Stress Evaluation

### 4.1 Inputs
- `energy` (inverse)
- `activation`
- `consecutive_fires`
- `apoptosis_risk`

### 4.2 Weights (default)
- energy: 0.35
- activation: 0.25
- firing: 0.20
- apoptosis_risk: 0.20

### 4.3 Levels
| Level | Threshold |
|---|---|
| low | < 0.25 |
| medium | 0.25 |
| high | 0.50 |
| critical | 0.75 |

## 5. Damage Evaluation

### 5.1 Accumulation
Damage accumulates with stress exposure and decays slowly:
`damage += accumulation_rate * stress_score`

### 5.2 Levels
| Level | Threshold | Repairable? |
|---|---|---|
| none | < 0.20 | n/a |
| reversible | 0.20 | yes (cheap) |
| functional | 0.40 | yes (moderate) |
| structural | 0.60 | rarely (expensive) |
| critical | 0.80 | no |

## 6. Repair Engine

### 6.1 Actions
- `reversible_repair`: heal 0.30, cost 0.05
- `functional_repair`: heal 0.10, cost 0.075
- `structural_repair`: heal 0.02, cost 0.15
- `critical_repair`: heal 0.00, cost 0.25

### 6.2 Budget constraint
Neuron must have `energy >= max(min_energy_to_repair, cost)`.

## 7. Defense Engine

### 7.1 Actions
- `snooze`: set snooze_counter, zero activation
- `firewall`: clear targets temporarily
- `quarantine`: clear targets, zero activation, drain energy

### 7.2 Thresholds (default)
- quarantine: stress >= 0.70 AND damage >= 0.60
- firewall: stress >= 0.50
- snooze: stress >= 0.60

### 7.3 Protected neurons
- `is_critical = True`
- `neuron_role in ("input", "output", "regulatory")`

## 8. Epigenetic Adapter

### 8.1 Gene categories
- metabolic: `metabolic_baseline`, `energy_efficiency`
- stress response: `hsp70_like`, `oxidative_stress_response`, `calcium_buffering`
- repair: `dna_repair_like`, `proteostasis`, `autophagy_like`
- defense: `immune_like_response`, `inflammatory_dampening`, `barrier_reinforcement`

### 8.2 Shift trigger
Stress and damage thresholds determine which genes are activated.
Shifts are recorded per-cell and persisted in `neuron.epigenetic_marks`.

## 9. Orchestrator Integration

T42 runs in `_tick()` after all regional and brainstem logic, before the morphology snapshot:

1. Evaluate stress
2. Evaluate damage (using previous damage state for continuity)
3. Run defense
4. Run repair
5. Run epigenetic adaptation

Flags:
- `cellular_adaptive_defense_enabled`
- `cellular_repair_enabled`
- `cellular_epigenetics_enabled`

## 10. Benchmark Metrics

| Metric | Source |
|---|---|
| mean_cellular_stress | stress_result.mean_stress |
| max_cellular_stress | stress_result.max_stress |
| mean_damage_score | damage_result.mean_damage |
| max_damage_score | damage_result.max_damage |
| repair_success_rate | repair_result.repair_success_rate |
| defense_activation_count | defense_result.defense_activation_count |
| quarantined_cell_count | defense_result.quarantined_count |
| epigenetic_shift_count | epigenetic_result.epigenetic_shift_count |
| cellular_resilience_score | composite: 0.3*(1-stress) + 0.4*(1-damage) + 0.3*repair_rate |

## 11. Acceptance Criteria

- 5 new cellular modules implementati e testati
- Orchestrator integration: T42 tick logic dopo energy control, prima di snapshot
- BenchmarkMetrics include 9 nuovi campi T42
- Markdown report include righe T42
- 25+ tests passano
- coverage >= 85%
- Commit + tag v0.3.26

## 12. Commit Tag

`v0.3.26-t42-cellular-adaptive-defense-repair`
