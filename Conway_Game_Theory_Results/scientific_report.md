# Phase 4 — Game-Theoretic Analysis of Conway’s Game of Life

## Design

We analyze two explicitly different 3×3 restricted strategy games on a finite 5×5 Conway B3/S23 board. Generation 1 is the initial configuration and Generation 10 follows nine synchronous updates. For each budget of 3–6 live cells per player, three deterministic strategy templates (Compact, Row-oriented, Dispersed) are selected in disjoint upper/lower placement regions. The empty central row may become occupied through Conway evolution.

**Model 1 (primary, zero-sum):** Player A maximizes N10; Player B minimizes N10. Payoffs are (N10, −N10).

**Model 2 (secondary, non-zero-sum):** Both players maximize their counterfactual contributions to final population. Payoffs are (N10(A∪B) − N10(B), N10(A∪B) − N10(A)). These are marginal-contribution utilities, not tracked ownership of individual cells.

## Results

| Cells/player | Total initial | Mean N10 | Zero-sum value | Zero-sum pure NE | Mutual pure NE | Mutual equilibrium representatives |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 6 | 2.111 | 0.000 | 3 | 2 | 3 |
| 4 | 8 | 4.000 | 0.000 | 3 | 2 | 3 |
| 5 | 10 | 4.000 | 3.158 | 0 | 3 | 7 |
| 6 | 12 | 3.556 | 0.000 | 3 | 1 | 1 |

## Interpretation and limitations

- These equilibria are valid **only within the selected three strategies per player**, not all possible 5×5 configurations.
- The spatial partition prevents overlapping initial choices but introduces location and boundary effects. It is a controlled design choice, not a claim of spatial neutrality.
- Strategy-family labels are operational labels selected by deterministic geometric scoring; the patterns are not universal representatives of all clustered/linear/dispersed structures.
- Model 2 does not create persistent ownership, competing cell species, or modify the B3/S23 transition rule.
- The sample includes 36 distinct joint initial configurations, each deterministic. No statistical inference over random strategy samples is justified.
- In degenerate non-zero-sum games, infinitely many equilibria may exist. The report enumerates feasible support representatives only.
- Phase 3 density–persistence results motivate the budgets but do not establish that any budget is optimal for this strategic design.

## Reproducibility

Run `py -m pip install numpy scipy matplotlib openpyxl`, then `py conway_game_theory_phase4.py`.
See `strategies.csv`, `all_pairings.csv`, `all_generations.csv`, `equilibria.csv`, `pure_nash.csv`, and `experiment_metadata.json` for full auditability.
