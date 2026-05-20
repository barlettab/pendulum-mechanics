import os
from pathlib import Path
import runpy

EXPERIMENT_FILES = [
    "exp1_sp_linear_real.py",
    "exp2_dp_linear_real.py",
    "exp3_dp-butterfly_effect.py",
    "exp4_divergence_time.py",
    "exp5_lyapunov_exponent.py",
    "exp6_predictability_horizon.py",
    "exp7_theils_predictability.n.py",
    "exp8_shannonentropy_comparison.py",
    "exp9_energy_conservation.py",
]


def run_experiment(script_path: Path) -> None:
    print("\n" + "=" * 60)
    print(f"Running: {script_path}")
    print("=" * 60)
    runpy.run_path(str(script_path), run_name="__main__")


def main() -> None:
    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    base = Path(__file__).resolve().parent / "experiments"
    for filename in EXPERIMENT_FILES:
        script = base / filename
        if not script.exists():
            raise FileNotFoundError(f"Experiment file not found: {script}")
        run_experiment(script)

    print("\nAll experiments completed.")


if __name__ == "__main__":
    main()
