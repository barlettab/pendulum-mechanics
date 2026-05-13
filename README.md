# Nonlinear Dynamics Lab: Pendulum Predictability & Chaos

This project is a computational laboratory for studying **nonlinear dynamics**, **predictability**, and **information loss** in physical systems, using the simple and double pendulum as canonical examples.

The goal is to explore how deterministic physical systems can become practically unpredictable due to sensitivity to initial conditions, and how this relates to concepts such as entropy, forecasting error, and chaos.

# Core Questions

This project investigates:

- How does predictability degrade over time in nonlinear systems?
- Why do small perturbations lead to large divergences?
- How does model complexity relate to uncertainty (entropy)?
- Can linear approximations predict nonlinear systems?
- How fast does information about the initial state get lost?


# Systems Studied

## Simple Pendulum
A nonlinear but regular dynamical system governed by:

\[
\theta'' + \frac{g}{L}\sin(\theta) = 0
\]

Used as a baseline for predictable oscillatory motion.


## Double Pendulum
A coupled nonlinear system exhibiting **chaotic behavior**.

Small differences in initial conditions lead to exponential divergence over time.


# Metrics

## 🔹 Theil’s U
Measures predictive accuracy compared to a naive model:

- U < 1 → model improves over baseline
- U ≈ 1 → no improvement
- U > 1 → worse than naive prediction


## 🔹 Entropy (Information Theory)
Measures uncertainty in the distribution of system states.

Higher entropy → more dispersion → less predictability.


## 🔹 Trajectory Divergence
Measures distance between two nearly identical initial conditions:

\[
d(t) = ||x_A(t) - x_B(t)||
\]

Used to demonstrate the **butterfly effect**.


## 🔹 Predictability Horizon
Measures how prediction error grows as forecast horizon increases.


# Experiments

| Experiment | Description |
|------------|-------------|
| exp1 | Linear vs nonlinear model comparison |
| exp2 | Butterfly effect (trajectory divergence) |
| exp3 | Exponential error growth |
| exp4 | Predictability horizon |
| exp5 | Entropy comparison between systems |



# Project Structure
    pendulum-mechanics/
    │
    ├── models/ # Modelos físicos dos sistemas
    ├── core/ # Métricas e utilidades
    ├── experiments/ # Experimentos científicos
    │
    ├── data/ # Dados numéricos salvos (.npy)
    ├── plots/ # Figuras geradas
    │
    ├── run_all.py # Pipeline principal
    └── README.md