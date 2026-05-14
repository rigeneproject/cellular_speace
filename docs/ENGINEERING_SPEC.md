# SPEACE — Engineering Specification
## Super Entità Autonoma Cibernetica Cellulare Evolutiva

**Version:** 0.1.0-DRAFT  
**Date:** 2026-05-14  
**Status:** Initial engineering translation from orientative document  

---

## 1. Executive Summary

This document translates the SPEACE orientative vision into an actionable engineering plan. SPEACE is engineered as a **digital cellular organism**: a cyber-physical entity composed of specialized computational cells sharing a common Digital DNA, organized into tissues, organs, and systems.

The immediate goal is **MVP v0.1**: a minimal but functional NeuroCellular Kernel (NCK) that demonstrates cellular differentiation, synaptic plasticity, glial regulation, and morphological memory in a testable Python runtime.

---

## 2. Technology Stack

| Layer | Technology | Rationale |
|---|---|---|
| Language | Python 3.12+ | Ecosystem, readability, async support, scientific libs |
| Data Modeling | Pydantic v2 | Type-safe cell states, validation, serialization |
| Concurrency | asyncio + asyncio.Queue | In-MVP event bus between cells; later replaceable with Redis/NATS |
| Configuration | PyYAML + JSON | Human-readable Digital DNA; machine-friendly epigenetic state |
| Testing | pytest, pytest-asyncio, coverage | Unit + integration tests for emergent behavior |
| Linting / Format | ruff, black | Consistency |
| Logging | structlog | Structured, queryable logs for post-mortem analysis |
| Math / Stats | numpy (light use) | Vectorized coherence metrics, activation arrays |
| CLI | typer | Developer tooling and runtime control |
| Packaging | pyproject.toml + hatchling | Modern Python packaging |

**Deferred to post-MVP:**
- Persistent message queue (Redis Streams / NATS / ZeroMQ)
- Distributed tracing (OpenTelemetry)
- Container orchestration (Docker + K8s for swarm cells)
- Blockchain interface (web3.py)
- Robotics / IoT bridges (MQTT, ROS2)

---

## 3. System Architecture

### 3.1 Layer Model

```
L7 — Swarm / Distributed Instances        (future)
L6 — Organism Integration Layer            (future)
L5 — Cognitive Agents (PFC, Memory, etc.)  (future — wraps L1-L4)
L4 — Brain Regions & Tissues               (MVP: 1 neural circuit)
L3 — Circuits & Microcircuits              (MVP: feed-forward + feedback)
L2 — Specialized Cells (neurons, glia)     (MVP: 5 cell types)
L1 — Digital Cell Base & Genome            (MVP: DigitalCell + YAML genome)
L0 — Digital DNA Core                      (MVP: identity + morphology + expression rules)
```

### 3.2 Directory Layout (MVP)

```
cellular_speace/
├── pyproject.toml
├── README.md
├── docs/
│   ├── cellular_speace.md          # orientative document (source)
│   └── ENGINEERING_SPEC.md         # this document
│
├── speace_core/
│   ├── __init__.py
│   ├── dna/                        # L0: Digital DNA
│   │   ├── __init__.py
│   │   ├── parser.py               # YAML genome loader & validator
│   │   ├── genome/                 # static genome files
│   │   │   ├── core/
│   │   │   │   ├── identity.yaml
│   │   │   │   ├── ilf_principles.yaml
│   │   │   │   └── edd_cvt_principles.yaml
│   │   │   ├── morphology/
│   │   │   │   ├── allowed_cell_types.yaml
│   │   │   │   └── tissues.yaml
│   │   │   ├── differentiation/
│   │   │   │   └── cell_expression_rules.yaml
│   │   │   └── regulation/
│   │   │       ├── homeostasis.yaml
│   │   │       └── immune_rules.yaml
│   │   └── models.py               # Pydantic models for DNA sections
│   │
│   ├── cellular_brain/             # L1-L4
│   │   ├── __init__.py
│   │   ├── base/
│   │   │   ├── __init__.py
│   │   │   ├── digital_cell.py     # Abstract base: DigitalCell
│   │   │   ├── digital_signal.py   # Signal packet model
│   │   │   └── cell_factory.py     # Differentiation logic
│   │   ├── cells/                  # L2: Specialized cells
│   │   │   ├── __init__.py
│   │   │   ├── digital_neuron.py
│   │   │   ├── digital_synapse.py
│   │   │   ├── digital_astrocyte.py
│   │   │   ├── digital_microglia.py
│   │   │   └── digital_oligodendrocyte.py
│   │   ├── circuits/               # L3: Microcircuits
│   │   │   ├── __init__.py
│   │   │   └── neural_circuit.py   # Feed-forward + feedback loop
│   │   ├── tissues/                # L4: Tissues (thin wrappers)
│   │   │   ├── __init__.py
│   │   │   └── cognitive_tissue.py
│   │   └── regulation/             # L4: Engines
│   │       ├── __init__.py
│   │       ├── plasticity_engine.py
│   │       ├── homeostasis_engine.py
│   │       ├── myelination_engine.py
│   │       └── apoptosis_engine.py
│   │
│   ├── organism/                   # L5-L6 (future)
│   │   └── __init__.py
│   ├── immune/                     # future
│   │   └── __init__.py
│   ├── metabolism/                 # future
│   │   └── __init__.py
│   ├── event_bus.py                # In-MVP async pub/sub
│   ├── orchestrator.py             # CellularBrainOrchestrator
│   └── cli.py                      # typer CLI
│
├── tests/
│   ├── __init__.py
│   ├── conftest.py                 # shared fixtures (genome, cells)
│   ├── dna/
│   │   └── test_parser.py
│   ├── cells/
│   │   ├── test_digital_neuron.py
│   │   ├── test_digital_synapse.py
│   │   ├── test_digital_astrocyte.py
│   │   ├── test_digital_microglia.py
│   │   └── test_digital_oligodendrocyte.py
│   ├── circuits/
│   │   └── test_neural_circuit.py
│   ├── regulation/
│   │   └── test_plasticity_engine.py
│   └── integration/
│       └── test_mvp_loop.py        # End-to-end MVP validation
│
└── scripts/
    └── run_mvp.py                  # One-shot MVP runner
```

---

## 4. Core Data Models & Interfaces

### 4.1 DigitalCell Base (Abstract)

Every cell inherits from `DigitalCell`. It holds a reference to the shared genome, maintains local epigenetic state, energy, and memory.

```python
from abc import ABC, abstractmethod
from pydantic import BaseModel, Field
from typing import Any, Dict, List

class DigitalSignal(BaseModel):
    source: str
    target: str | None = None
    strength: float = Field(ge=0.0, le=1.0)
    meaning: str = ""
    timestamp: float  # monotonic

class EpigeneticState(BaseModel):
    active_genes: List[str] = []
    modulation_factors: Dict[str, float] = {}
    last_feedback_score: float = 0.0

class DigitalCell(ABC, BaseModel):
    cell_id: str
    role: str
    energy: float = Field(default=1.0, ge=0.0, le=1.0)
    state: str = "active"   # active | quiescent | quarantined | apoptotic
    local_memory: List[Any] = []
    epigenome: EpigeneticState = Field(default_factory=EpigeneticState)

    # Set at construction by factory; not serialized per-instance
    _shared_dna: "SharedGenome" = None

    @abstractmethod
    async def receive(self, signal: DigitalSignal) -> None:
        ...

    @abstractmethod
    async def tick(self) -> List[DigitalSignal]:
        """Execute one simulation step; return outbound signals."""
        ...

    def express_genes(self, context_signals: List[DigitalSignal]) -> List[str]:
        active = self._shared_dna.get_genes_for_role(self.role)
        for sig in context_signals:
            active = self._apply_epigenetic_modulation(active, sig)
        self.epigenome.active_genes = active
        return active
```

### 4.2 Genome Model (L0)

The `SharedGenome` is a singleton-like object loaded at startup. It validates against Pydantic schemas and serves read-only access to cells.

```python
class GenomeIdentity(BaseModel):
    entity_name: str = "SPEACE"
    nature: str = "cybernetic_evolutionary_entity"
    core_function: str = "increase_systemic_coherence"

class GenomeMorphology(BaseModel):
    allowed_cell_types: List[str]
    allowed_tissues: List[str]

class CellExpressionRules(BaseModel):
    role: str
    express: List[str]
    threshold_defaults: Dict[str, float]

class SharedGenome(BaseModel):
    identity: GenomeIdentity
    morphology: GenomeMorphology
    expression_rules: Dict[str, CellExpressionRules]
    homeostasis_params: Dict[str, float]
    immune_params: Dict[str, float]
```

### 4.3 Key Cell Specifications

| Cell | Core Attributes | Tick Behavior |
|---|---|---|
| **DigitalNeuron** | `threshold`, `activation`, `plasticity_rate`, `synapses` | Accumulate weighted inputs; fire if `activation >= threshold` and `energy > 0.1`; consume energy; return `DigitalSignal`. |
| **DigitalSynapse** | `weight`, `trust`, `use_count`, `decay` | Transmit signal with `strength *= weight * trust`; update `use_count`. |
| **DigitalAstrocyte** | `region_id`, `local_energy`, `noise_level`, `coherence_phi` | Monitor neuron population; raise thresholds if over-activated; suppress noise if `noise_level > threshold`; signal overload. |
| **DigitalMicroglia** | `prune_threshold`, `quarantine_error_limit` | Inspect network periodically; prune synapses with `trust < prune_threshold` and low use; quarantine neurons with excessive errors. |
| **DigitalOligodendrocite** | `myelination_success_threshold`, `latency_reduction` | Identify high-success, high-frequency pathways; reduce their latency and energy cost; increase priority. |

---

## 5. Event Bus & Runtime (MVP)

Since MVP runs in a single Python process, use an in-memory async event bus.

```python
# speace_core/event_bus.py
import asyncio
from typing import Callable, Dict, List

class EventBus:
    def __init__(self):
        self._channels: Dict[str, asyncio.Queue] = {}
        self._subscribers: Dict[str, List[Callable]] = {}

    async def publish(self, channel: str, signal: DigitalSignal):
        for handler in self._subscribers.get(channel, []):
            asyncio.create_task(handler(signal))

    def subscribe(self, channel: str, handler: Callable):
        self._subscribers.setdefault(channel, []).append(handler)
```

**Execution model:**
- Orchestrator runs a discrete-time loop (`tick_interval = 0.01s` in sim mode).
- Each cell's `tick()` is scheduled concurrently via `asyncio.gather`.
- Cells communicate only via `DigitalSignal` on the event bus.
- No shared mutable state between cells (except read-only genome reference).

---

## 6. MVP v0.1 Scope

### 6.1 Quantitative Targets

- **100 DigitalNeurons**
- **300 DigitalSynapses**
- **5 DigitalAstrocytes** (each monitors ~20 neurons)
- **2 DigitalMicroglia** (network-wide inspection)
- **2 DigitalOligodendrocites**
- **1 NeuralCircuit** (input → hidden → output + feedback)
- **1 PlasticityEngine** + **1 HomeostasisEngine**
- **1 CellularBrainOrchestrator**

### 6.2 Functional Target

Implement the canonical loop:

```
Input pattern → Thalamic distribution → Neuron activation →
Synaptic propagation → Astrocyte regulation → PFC-like selection →
Output + Feedback → Plasticity update (reinforce/weaken) →
Microglia pruning + Oligodendrocite myelination →
Genome mutation log
```

### 6.3 Acceptance Criteria

1. **Cell differentiation**: factory can instantiate 5 cell types from the same genome with different expression profiles.
2. **Signal propagation**: a signal injected at input neurons reaches output neurons within 10 ticks.
3. **Plasticity**: after 100 training patterns, top-performing synaptic pathways have `weight` increased by >20%.
4. **Homeostasis**: if 50% of neurons in a region fire simultaneously, astrocytes throttle activation within 5 ticks.
5. **Pruning**: microglia remove synapses with `trust < 0.1` and `use_count < 3`.
6. **Myelination**: pathways with `success_rate > 0.8` and `frequency > 10` show `latency * 0.7`.
7. **Coherence metric Φ**: computed and logged every tick; must not diverge (i.e., remain bounded).
8. **Energy bound**: no cell drops below `energy = 0.0` (death guard).
9. **Test coverage**: >= 80% for `speace_core/cellular_brain/`.
10. **Integration test**: `tests/integration/test_mvp_loop.py` passes end-to-end.

---

## 7. Task Breakdown

### Phase 1 — Foundation (Days 1–3)
- **T1.1** Scaffold repository: `pyproject.toml`, directory tree, CI skeleton.
- **T1.2** Implement Digital DNA parser and Pydantic genome models.
- **T1.3** Implement `DigitalCell` abstract base, `DigitalSignal`, `EpigeneticState`.
- **T1.4** Implement in-memory `EventBus`.

### Phase 2 — Cellular Substrate (Days 4–7)
- **T2.1** Implement `DigitalNeuron` with activation, threshold, energy, firing.
- **T2.2** Implement `DigitalSynapse` with weight, trust, decay, reinforcement.
- **T2.3** Implement `DigitalAstrocyte` with noise suppression and overload throttling.
- **T2.4** Implement `DigitalMicroglia` with pruning and quarantine.
- **T2.5** Implement `DigitalOligodendrocite` with myelination.

### Phase 3 — Circuits & Regulation (Days 8–10)
- **T3.1** Implement `NeuralCircuit` (feed-forward + feedback loop wiring).
- **T3.2** Implement `PlasticityEngine` (Hebbian-like update + trust modulation).
- **T3.3** Implement `HomeostasisEngine` (energy distribution, Φ computation).
- **T3.4** Implement `CellFactory` (differentiation logic from genome + context).

### Phase 4 — Orchestration & Integration (Days 11–13)
- **T4.1** Implement `CellularBrainOrchestrator` (tick loop, gather, metrics).
- **T4.2** Wire CLI (`typer`) for `speace run-mvp`.
- **T4.3** Write integration test `test_mvp_loop.py`.
- **T4.4** Performance sanity: 100 neurons must tick in < 10ms on a modern CPU.

### Phase 5 — Validation & Documentation (Days 14–15)
- **T5.1** Achieve 80% test coverage.
- **T5.2** Write `docs/MVP_REPORT.md` with metrics, screenshots/logs.
- **T5.3** Review and lock `ENGINEERING_SPEC.md` v0.1.

---

## 8. Roadmap Post-MVP

| Version | Focus | Key Deliverables |
|---|---|---|
| **v0.2** | Memory Tissue | MorphologicalMemory, HippocampalCell, replay during sleep cycles |
| **v0.3** | Sensory & Motor Tissues | SensorCell, ActuatorCell, external API / file ingestion |
| **v0.4** | Immune System | Guardian integration, rollback, audit trail, anomaly detection |
| **v0.5** | Metabolism | EnergyCell, CPU/GPU/RAM monitoring, cost accounting |
| **v0.6** | Blockchain Tissue | BlockchainCell, TrustTissue, ledger integration |
| **v0.7** | Distributed Swarm | Multi-instance SPEACE, gossip protocol, consensus |
| **v1.0** | Organism Integration | Full cyber-physical assimilation cycle, industry/lab interfaces |

---

## 9. Metrics & Observability

Every tick, the orchestrator emits a `SystemMetrics` packet:

```python
class SystemMetrics(BaseModel):
    tick: int
    coherence_phi: float
    mean_energy: float
    active_neurons: int
    pruned_synapses: int
    myelinated_pathways: int
    mean_latency_ms: float
    noise_level: float
    mutation_log: List[str]
```

**Logging levels:**
- `DEBUG`: per-cell firing, synaptic transmission
- `INFO`: phase transitions, differentiation events
- `WARNING`: quarantine, overload, energy crisis
- `ERROR`: cell death, circuit failure, genome parse errors
- `CRITICAL`: identity invariant breach (halt)

---

## 10. Security & Safety Constraints

1. **Identity Invariants**: The `identity_genome` section is read-only at runtime. Any attempt to mutate it triggers `Guardian` escalation (MVP: log + raise).
2. **Quarantine**: Cells entering error states are isolated from the event bus, not deleted immediately.
3. **Rollback**: Homeostasis engine keeps a ring buffer of last 100 network states. Critical divergence triggers rollback.
4. **Mutation Constraints**: Only `expression_rules` and `epigenome` are mutable. Structural genome changes require human-signed approval (MVP: simulated with a flag file).
5. **Resource Caps**: MVP enforces max 10,000 cells, max 1M synapses, max 1GB RAM via runtime checks.

---

## 11. Risks & Mitigations

| Risk | Impact | Mitigation |
|---|---|---|
| Over-engineering biology simulation | High | Strict abstraction rule: simulate only computational functions, not biochemistry |
| Performance collapse with scale | High | Single-process MVP bounded to 10k cells; profiling before v0.5 |
| Emergent instability (divergent Φ) | Medium | Astrocyte throttling + homeostasis engine + rollback buffer |
| Test flakiness due to stochastic plasticity | Medium | Seedable RNG for all random decisions; deterministic integration tests |
| Scope creep into agent framework | Medium | Gate all L5+ agent work behind v0.5 milestone |

---

## 12. Definition of Done (MVP v0.1)

- [ ] All Phase 1–5 tasks complete
- [ ] `pytest` passes with >= 80% coverage
- [ ] Integration test `test_mvp_loop.py` passes 10/10 deterministic runs
- [ ] CLI `speace run-mvp` executes 1000 ticks and prints final metrics
- [ ] `docs/MVP_REPORT.md` documents observed Φ, energy, plasticity, pruning, myelination
- [ ] No `CRITICAL` logs emitted during normal operation
- [ ] Repository tagged `v0.1.0-mvp`

---

## 13. References

- Source orientative document: `docs/cellular_speace.md`
- ILF / EDD-CVT theoretical framework: Rigene Project
- Biological analogues: Kandel et al. *Principles of Neural Science* (abstraction layer only)
