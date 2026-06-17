# Implementazione dei meccanismi neurali, sinaptici e quantistici in SPEACE

Questo documento riassume lo stato di implementazione dei requisiti
neurali/sinaptici/quantistici di SPEACE e i gap colmati in questa fase.

## 1. Neuroni e sinapsi come classi Pydantic

- `speace_core/cellular_brain/cells/digital_neuron.py` — `DigitalNeuron(DigitalCell)`
- `speace_core/cellular_brain/cells/digital_synapse.py` — `DigitalSynapse(DigitalCell)`
- Campi tipizzati: soglia, attivazione, peso, trust, plasticità, periodo refrattario, microstati COR.
- Ciclo `tick()` in `NeuralCircuit.tick()`.

## 2. Rappresentazione parametrica, gerarchica e lazy

- Il DNA in `speace_core/dna/models.py` e `speace_core/dna/genome/default_genome.yaml`
  definisce tipi cellulari, regole di espressione, differenziazione regionale e
  geni del connettoma (`connectome_genes`).
- `CellFactory` crea neuroni in base al contesto, senza istanziare miliardi di oggetti.
- `FunctionalActivationGate` attiva funzioni latenti solo quando arriva un segnale
  con un significato compatibile (on-demand).

## 3. Tavola periodica neurale-sinaptica guidata dal DNA

- `speace_core/cellular_brain/neuroperiodic/` implementa elementi neurali, legami
  sinaptici, leggi periodiche e un integratore con la tavola periodica.
- **Novità**: `PeriodicLaw.from_genome()` carica trend, regole valenza e reazioni
  direttamente dal Digital DNA (`periodic_table_genes` in `SharedGenome`).
- `NeuroPeriodicIntegrator.from_genome()` usa queste leggi DNA-driven per predire
  sinapsi e classificare cellule.

## 4. Meccanismi atomici, fisica e quantistica

- Strato quantistico simulato in `speace_core/cellular_brain/quantum/`:
  `QuantumState`, `QuantumBrainSimulator`, `QuantumNeuralBridge`.
- Strato di risonanza in `speace_core/cellular_brain/resonance/`:
  `ResonanceField`, `WaveInterferenceEngine`, `PauliExclusionEngine`.
- Dualità onda-particella in `DigitalNeuron` (`wave_phase`, `wave_amplitude`).
- **Novità**: `QuantumGeneSet` nel DNA configura il ponte quantistico, inclusa una
  mappa `periodic_element_qubit_map` che collega blocchi della tavola periodica a
  capacità qubit.

## 5. Simulatori integrati

- `speace_core/cellular_brain/simulator_backends/` contiene:
  - `NativeBackend` (default, zero dipendenze)
  - `Brian2Backend`
  - `NESTBackend`
  - `NEURONBackend`
  - `BackendSelector` e astrazione `Population`/`Projection` PyNN-like.
- **Novità**: il `CellularBrainOrchestrator` può abilitare un backend esterno
  (`simulator_backend_enabled`, `simulator_backend_name`) e sincronizzare lo stato
  del circuito con esso a intervalli configurabili.

## Gap colmati in questa fase

1. DNA regola attivamente la tavola periodica (trend, valence rules, reactions).
2. Simulatori Brian2/NEST/NEURON sono collegati al ciclo dell'orchestrator.
3. Implementato `FunctionalActivationGate` per attivazione lazy on-demand.
4. Aggiunti `QuantumGeneSet` e mappatura periodica-qubit nel DNA.

## Limiti noti

- La fisica quantistica è un'emulazione classica; non c'è coerenza quantistica reale.
- I backend esterni richiedono le rispettive librerie Python installate.
- Il wiring con l'orchestrator è attualmente un probe periodico; un'integrazione
  più profonda (sostituzione del tick nativo) può essere aggiunta in futuro.

## Gap colmati in questa fase di verifica e completamento

1. **Fix stabilità HomeostasisEngine**: `_compute_phi` ora normalizza usando il
   valore assoluto delle attivazioni, evitando il crash `math.log` su probabilità
   negative quando le attivazioni sono negative.
2. **COR diventa DNA-driven**: aggiunto `CORGeneSet` in `speace_core/dna/models.py`
   e campo `cor_genes` in `SharedGenome`; `CellularBrainOrchestrator.build_mvp`
   applica automaticamente i parametri COR dal genome quando `enabled: true`.
3. **Nuovo compito/ambiente esterno**: `AssociativeRecallEnvironment` in
   `speace_core/environment/associative_recall_environment.py` testa la memoria
   associativa con fase di studio e fase di test; integrato in `EnvironmentAdapter`
   e nel launcher `run_speace_with_environment.py`.
4. **Test di integrazione**: aggiunti test per `AssociativeRecallEnvironment`
   e per `QuantumNeuralBridge`.
5. **Verifica funzionale**: 249+ test rilevanti passano; i launcher
   `run_speace_brain.py`, `run_speace_with_environment.py prediction/grid/associative`
   producono report coerenti.

## Come avviare il cervello con rappresentazione parametrica/lazy

```powershell
cd C:\cellular_speace
python run_speace_brain.py
python run_speace_with_environment.py prediction
python run_speace_with_environment.py grid
python run_speace_with_environment.py associative
```

Il cervello non materializza miliardi di neuroni: usa `DigitalNeuron`/`DigitalSynapse`
come classi Pydantic e il `FunctionalActivationGate` per attivare funzioni latenti
(e microstati COR) solo quando un segnale con un significato compatibile arriva.
La tavola periodica neurale-sinaptica e i geni COR/quantistici nel DNA guidano
comportamento, plasticità e collassi metacognitivi.
