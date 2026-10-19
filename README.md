# Conway's Game of Life: Game Theory Prototype

A reproducible Python prototype exploring strategic interactions in Conway's Game of Life through payoff matrices and pure-strategy Nash equilibrium analysis.

## Overview

This project investigates a simple two-player strategic game based on Conway's Game of Life, a cellular automaton governed by deterministic transition rules.

Each player selects one of three predefined initial configurations. The selected configurations are combined into a single finite grid, which evolves according to Conway's classical rules. The resulting number of living cells determines each player's payoff.

The prototype provides a graphical interface for exploring the simulation, evaluating strategy combinations, and identifying pure-strategy Nash equilibria.

## Research Objectives

- Explore strategic interactions in a cellular automaton.
- Model a two-player zero-sum game using predefined initial configurations.
- Compute the payoff matrix for all possible strategy combinations.
- Identify pure-strategy Nash equilibria, if they exist.
- Provide a reproducible computational tool for discussing and refining the mathematical model.

## Model Assumptions

The current implementation uses the following provisional assumptions:

| Parameter | Definition |
|---|---|
| Players | 2 |
| Grid size | 5 × 5 cells |
| Available strategies | 3 per player |
| Simulation horizon | 10 generations |
| Boundary conditions | Cells outside the grid are permanently dead |
| Initial configuration | Union of both players' selected cell sets |
| Player A's utility | Number of living cells at generation 10 |
| Player B's utility | Negative of Player A's utility |
| Game type | Two-player zero-sum game |

The payoff functions are:

\[
U_A(s_A,s_B)=N_{10}(s_A,s_B)
\]

\[
U_B(s_A,s_B)=-N_{10}(s_A,s_B)
\]

where \(N_{10}\) denotes the number of living cells after ten generations.

## Available Strategies

The prototype includes three illustrative initial configurations:

- **S1 — 2×2 Block:** Four living cells arranged in a square.
- **S2 — Horizontal Line of 3:** Three adjacent living cells.
- **S3 — Short Diagonal:** Three living cells arranged diagonally.

These configurations are experimental choices, not established optimal strategies.

## Features

- Graphical visualization of the 5×5 cellular automaton.
- Interactive selection of both players' strategies.
- Step-by-step progression through successive generations.
- Automatic calculation of all nine strategy combinations.
- Payoff matrix generation.
- Best-response analysis for both players.
- Identification of pure-strategy Nash equilibria.
- Explicit documentation of model assumptions and limitations.

## Requirements

- Python 3.9 or later recommended.
- Tkinter, generally included with standard Python installations.
- No external Python packages are required.

On some Linux distributions, Tkinter may need to be installed separately.

## Installation and Execution

Clone the repository:

```bash
git clone https://github.com/YOUR-USERNAME/conway-life-game-theory.git
cd conway-life-game-theory
```

Run the application:

```bash
python main.py
```

On some systems, use:

```bash
python3 main.py
```

## How to Use

1. Launch the application.
2. Select an initial configuration for Player A.
3. Select an initial configuration for Player B.
4. Click **Simulate Combination** to display the initial configuration.
5. Click **Next Generation** to advance the simulation one generation at a time.
6. Click **Calculate Payoff Matrix and Equilibria** to evaluate all nine combinations.
7. Review the payoff matrix, best responses, and any pure-strategy Nash equilibria found.

## Nash Equilibrium Analysis

A pure-strategy Nash equilibrium is a strategy combination in which neither player can improve their own payoff through a unilateral deviation.

For this zero-sum game, Player A maximizes the number of living cells, while Player B minimizes that number.

The implementation identifies strategy combinations that are mutual best responses. If no pure-strategy equilibrium exists, the program reports that result without ruling out the existence of a mixed-strategy equilibrium.

## Project Structure

```text
conway-life-game-theory/
├── main.py
├── README.md
├── .gitignore
└── LICENSE
```

## Limitations

This implementation is an experimental prototype, not a validated scientific model.

Its conclusions are conditional on the selected strategies, finite grid, boundary conditions, utility function, and simulation horizon.

In particular:

- Only three initial configurations are available to each player.
- The union operation means overlapping living cells are counted only once.
- The payoff is evaluated at a single terminal generation.
- No mixed-strategy equilibrium solver is currently implemented.
- No claim is made that the selected strategies are globally optimal or representative of all possible configurations.

The model assumptions and experimental design should be reviewed before using the results to support scientific conclusions.

## Future Work

Potential extensions include:

- Formal validation of the game model and its assumptions.
- Systematic generation of additional initial configurations.
- Sensitivity analysis over