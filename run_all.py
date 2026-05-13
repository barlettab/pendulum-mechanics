import os
import importlib


EXPERIMENTS = [
    "pendulum_mechanics.experiments.exp1_model_error",
    "pendulum_mechanics.experiments.exp2_butterfly_effect",
    "pendulum_mechanics.experiments.exp3_divergence_time",
    "pendulum_mechanics.experiments.exp4_predictability_horizon",
    "pendulum_mechanics.experiments.exp5_entropy_comparison",
]


def run_experiment(module_name):

    print("\n" + "="*60)
    print(f"Running: {module_name}")
    print("="*60)

    module = importlib.import_module(module_name)

    # padrão científico: cada exp tem função run()
    module.run()


def main():

    os.makedirs("data", exist_ok=True)
    os.makedirs("plots", exist_ok=True)

    for exp in EXPERIMENTS:
        run_experiment(exp)

    print("\nAll experiments completed.")


if __name__ == "__main__":
    main()