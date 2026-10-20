# Phase 6 — Spatial Sensitivity of Restricted Conway Games

- Master seed: 20261020
- Independent strategy sets per budget: 40
- Budgets: [3, 4, 5, 6, 7]
- Transformations: identity, horizontal reflection, cyclic one-column shift, row swap
- Every independent set is evaluated under 16 paired transformations.
- **Important:** 16 transformations of the same strategy set are correlated observations.

## Results

| Cells per player | Games | No pure NE | Sets with equilibrium-status changes | Mean within-set value range |
|---:|---:|---:|---:|---:|
| 3 | 640 | 12.3% | 65.0% | 3.811 |
| 4 | 640 | 47.3% | 100.0% | 6.354 |
| 5 | 640 | 39.2% | 97.5% | 6.146 |
| 6 | 640 | 45.0% | 100.0% | 6.623 |
| 7 | 640 | 55.9% | 100.0% | 7.956 |

## Interpretation

Changes in pure-equilibrium status under fixed-budget transformations provide evidence of spatial sensitivity within sampled restricted 3x3 games. These are not equilibria of the full 5x5 strategy space.

## Methodological limitations

- Placement regions are fixed, disjoint, and separated by an initially empty middle row.
- The transformations are bijections of placement regions, not necessarily symmetries of the complete Conway board.
- Strategy sets are randomly sampled, and no exhaustive equilibrium claim is made.
- Secondary mutual-preservation model reports pure equilibria only; mixed equilibria are not solved.
- The primary zero-sum utility is a modeling choice, not a built-in competitive rule of Conway.
- Budget effects cannot be separated fully from changing reachable pattern geometry without further controls.

## Reproducibility

The CSV files contain the full strategy masks, board rows, payoff pairings, and equilibrium summaries. Re-run the script with the same seed and sample count to reproduce the outputs.
