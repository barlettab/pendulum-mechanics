from __future__ import annotations

import os
from pathlib import Path
import runpy
from dataclasses import dataclass, field


@dataclass(frozen=True)
class ExperimentSpec:
    id: int
    script: str
    output_dirs: list[str] = field(default_factory=list)
    requires_files: list[str] = field(default_factory=list)


EXPERIMENTS: list[ExperimentSpec] = [
    ExperimentSpec(1, "exp1_sp_linear_real.py", ["data/exp1", "plots/exp1"]),
    ExperimentSpec(2, "exp2_dp_linear_real.py", ["data/exp2", "plots/exp2"]),
    ExperimentSpec(3, "exp3_dp-butterfly_effect.py", ["data/exp3", "plots/exp3"]),
    ExperimentSpec(4, "exp4_divergence_time.py", ["data/exp4", "plots/exp4"]),
    ExperimentSpec(
        5,
        "exp5_lyapunov_exponent.py",
        ["data/exp5", "plots/exp5"],
        requires_files=[
            "data/exp4/theta1_A.npy",
            "data/exp4/theta2_A.npy",
            "data/exp4/theta1_B.npy",
            "data/exp4/theta2_B.npy",
        ],
    ),
    ExperimentSpec(6, "exp6_predictability_horizon.py", ["data/exp6", "plots/exp6"]),
    ExperimentSpec(7, "exp7_theils_predictability.n.py", ["data/exp7", "plots/exp7"]),
    ExperimentSpec(8, "exp8_shannonentropy_comparison.py", ["data/exp8", "plots/exp8"]),
    ExperimentSpec(9, "exp9_energy_conservation.py", ["data/exp9", "plots/exp9"]),
]


def validate_inputs(base_dir: Path, spec: ExperimentSpec) -> None:
    missing = [p for p in spec.requires_files if not (base_dir / p).exists()]
    if missing:
        missing_txt = "\n - ".join(missing)
        raise FileNotFoundError(
            f"exp{spec.id} requires input files that were not found:\n - {missing_txt}"
        )


def run_experiment(base_dir: Path, spec: ExperimentSpec) -> None:
    script_path = base_dir / "experiments" / spec.script
    if not script_path.exists():
        raise FileNotFoundError(f"Experiment script not found for exp{spec.id}: {script_path}")

    for folder in spec.output_dirs:
        os.makedirs(base_dir / folder, exist_ok=True)

    validate_inputs(base_dir, spec)

    print("\n" + "=" * 72)
    print(f"Running exp{spec.id}: {script_path}")
    print("=" * 72)
    runpy.run_path(str(script_path), run_name="__main__")


def main() -> None:
    base_dir = Path(__file__).resolve().parent
    os.makedirs(base_dir / "data", exist_ok=True)
    os.makedirs(base_dir / "plots", exist_ok=True)

    for spec in EXPERIMENTS:
        run_experiment(base_dir, spec)

    print("\nAll experiments completed.")


if __name__ == "__main__":
    main()
