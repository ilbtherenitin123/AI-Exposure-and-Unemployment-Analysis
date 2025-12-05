Create code/MonteCarlo_Unemployment_Scenarios.py (you can later copy into a notebook):
"""
MonteCarlo_Unemployment_Scenarios.py

Author: Nitin Ranjan

Description:
    Simple Monte Carlo framework to map AI exposure (share of workers
    in high-exposure occupations) into unemployment and labor-force-exit
    trajectories over time, using activation rates and institutional
    adjustment parameters grounded in the empirical literature.
"""

import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Core simulation function
# -----------------------------

def simulate_unemployment_path(
    exposure,
    activation,
    unemp_ratio,
    reemployment_rate,
    T=20,
):
    """
    Simulate unemployment and labor-force-exit paths given:

    exposure          : share of total employment in high-exposure occupations
    activation        : share of exposed workers displaced over the horizon
    unemp_ratio       : share of displaced workers that enter unemployment
                        (remainder exit the labor force / NILF)
    reemployment_rate : annual re-employment rate for unemployed workers
    T                 : number of years to simulate

    Returns:
        (unemployment_path, nilf_path) as numpy arrays of length T
    """

    displaced_total = exposure * activation
    displaced_per_year = displaced_total / T

    unemployment_path = []
    nilf_path = []

    current_unemp = 0.0
    current_nilf = 0.0

    for t in range(T):
        # New displacement this year
        new_unemp = displaced_per_year * unemp_ratio
        new_nilf = displaced_per_year * (1.0 - unemp_ratio)

        # Reemployment from existing unemployed
        reemp = reemployment_rate * current_unemp

        current_unemp = current_unemp + new_unemp - reemp
        current_nilf = current_nilf + new_nilf

        unemployment_path.append(current_unemp)
        nilf_path.append(current_nilf)

    return np.array(unemployment_path), np.array(nilf_path)


# -----------------------------
# Baseline scenario
# -----------------------------

if __name__ == "__main__":
    # Example: high-income country at 8% exposure (Gradients 3+4)
    exposure = 0.08

    # Baseline activation: 20% of exposed workers displaced over 20 years
    activation = 0.20

    # Weak-institution ratio from Autor et al. (2013), Jacobson et al. (1993):
    # ~29% to unemployment, ~71% NILF
    unemp_ratio = 0.29

    # Annual re-employment rate (weak-institution baseline)
    reemployment_rate = 0.15

    T = 20

    u_path, n_path = simulate_unemployment_path(
        exposure=exposure,
        activation=activation,
        unemp_ratio=unemp_ratio,
        reemployment_rate=reemployment_rate,
        T=T,
    )

    years = np.arange(1, T + 1)

    plt.figure()
    plt.plot(years, 100 * u_path, label="Unemployment", linewidth=2)
    plt.plot(years, 100 * n_path, label="Labor-force exit (NILF)", linewidth=2)
    plt.xlabel("Years")
    plt.ylabel("Percent of total employment")
    plt.title("AI-Induced Labor Market Adjustment (Baseline Scenario)")
    plt.legend()
    plt.grid(True)
    plt.tight_layout()
    plt.show()

    # -------------------------
    # Simple Monte Carlo on activation
    # -------------------------

    runs = 5000
    activation_mu = 0.20
    activation_sd = 0.05

    terminal_unemp = []

    rng = np.random.default_rng(seed=42)

    for _ in range(runs):
        a_draw = rng.normal(activation_mu, activation_sd)
        a_draw = float(np.clip(a_draw, 0.0, 1.0))

        u_mc, _ = simulate_unemployment_path(
            exposure=exposure,
            activation=a_draw,
            unemp_ratio=unemp_ratio,
            reemployment_rate=reemployment_rate,
            T=T,
        )
        terminal_unemp.append(u_mc[-1])

    terminal_unemp = np.array(terminal_unemp)

    mean_u = terminal_unemp.mean()
    p5, p95 = np.percentile(terminal_unemp, [5, 95])

    print("Terminal unemployment (as share of labor force):")
    print("  Mean:  {:.3%}".format(mean_u))
    print("  5th percentile:  {:.3%}".format(p5))
    print("  95th percentile: {:.3%}".format(p95))
