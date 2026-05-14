import asyncio
import pathlib
from typing import Optional

import typer

from speace_core.dna.parser import load_genome
from speace_core.orchestrator import CellularBrainOrchestrator

app = typer.Typer(name="speace", help="SPEACE Cellular Brain CLI")


@app.command()
def run_mvp(
    ticks: int = typer.Option(1000, "--ticks", "-t", help="Number of ticks to run"),
    genome_path: Optional[pathlib.Path] = typer.Option(
        None, "--genome", "-g", help="Path to genome YAML"
    ),
    patterns: int = typer.Option(100, "--patterns", "-p", help="Training patterns"),
) -> None:
    """Run the SPEACE MVP cellular brain."""
    if genome_path is None:
        genome_path = (
            pathlib.Path(__file__).resolve().parent / "dna" / "genome" / "default_genome.yaml"
        )
    genome = load_genome(genome_path)
    orchestrator = CellularBrainOrchestrator.build_mvp(genome)

    async def _run() -> None:
        typer.echo(f"Starting SPEACE MVP for {ticks} ticks...")
        for i in range(patterns):
            pattern = [0.0] * 10
            pattern[i % 10] = 1.0
            orchestrator.inject(pattern)
            await orchestrator.run_ticks(1)
            score = 1.0 if i % 2 == 0 else -0.2
            orchestrator.feedback(score)
            if i % 10 == 0:
                orchestrator.run_immune()
            metrics = orchestrator.latest_metrics
            if metrics:
                typer.echo(
                    f"Tick {metrics.tick:04d} | "
                    f"Phi={metrics.coherence_phi:.3f} | "
                    f"Energy={metrics.mean_energy:.3f} | "
                    f"Active={metrics.active_neurons} | "
                    f"Pruned={metrics.pruned_synapses}"
                )
        # final burn-in
        await orchestrator.run_ticks(ticks - patterns)
        final = orchestrator.latest_metrics
        if final:
            typer.echo("\n=== Final Metrics ===")
            typer.echo(f"Tick: {final.tick}")
            typer.echo(f"Coherence Phi: {final.coherence_phi:.4f}")
            typer.echo(f"Mean Energy: {final.mean_energy:.4f}")
            typer.echo(f"Active Neurons: {final.active_neurons}")
            typer.echo(f"Pruned Synapses: {final.pruned_synapses}")

    asyncio.run(_run())


if __name__ == "__main__":
    app()
