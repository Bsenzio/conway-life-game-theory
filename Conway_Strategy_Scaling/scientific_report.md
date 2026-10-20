# Phase 7 — Strategy-Space Scaling in a Fixed 5×5 Cellular Automaton

## Abstract

This study evaluates 1,500 finite zero-sum games and 67,000 deterministic strategy pairings on an unchanged 5×5 Conway B3/S23 board. The number of available actions per player is varied (3, 5, 10), while the cell budget is controlled (3–7 cells/player). Strategy sets are nested within each independently sampled 10-action set.

## Methods

- The board is 5×5 with dead exterior boundaries.
- Generation 1 is the initial configuration; Generation 10 follows nine synchronous updates.
- Player A seeds the top two rows and maximizes the final live-cell count.
- Player B seeds the bottom two rows and minimizes that same count.
- Each player selects distinct fixed-cardinality seed patterns.
- For each budget and sample, one 10×10 matrix is drawn; its upper-left 3×3 and 5×5 subgames are evaluated.
- Minimax equilibria are solved with primal and dual linear programs (SciPy HiGHS).
- Pure equilibria are matrix entries that are simultaneously a column maximum and row minimum.
- Wilson 95% intervals describe the proportion of sampled games lacking pure equilibria.

## Results

| Cells/player | Actions/player | No pure NE | No pure NE (%) | Mean minimax | Mean pure NE |
|---:|---:|---:|---:|---:|---:|
| 3 | 3 | 15/100 | 15.0 | 0.985 | 3.890 |
| 3 | 5 | 31/100 | 31.0 | 1.050 | 6.480 |
| 3 | 10 | 51/100 | 51.0 | 1.288 | 9.500 |
| 4 | 3 | 36/100 | 36.0 | 2.539 | 1.720 |
| 4 | 5 | 74/100 | 74.0 | 2.747 | 1.130 |
| 4 | 10 | 96/100 | 96.0 | 3.049 | 0.400 |
| 5 | 3 | 39/100 | 39.0 | 2.284 | 1.600 |
| 5 | 5 | 74/100 | 74.0 | 2.478 | 1.280 |
| 5 | 10 | 94/100 | 94.0 | 2.612 | 0.600 |
| 6 | 3 | 42/100 | 42.0 | 3.050 | 1.500 |
| 6 | 5 | 72/100 | 72.0 | 2.829 | 1.340 |
| 6 | 10 | 94/100 | 94.0 | 3.016 | 0.600 |
| 7 | 3 | 53/100 | 53.0 | 3.229 | 1.160 |
| 7 | 5 | 85/100 | 85.0 | 3.599 | 0.480 |
| 7 | 10 | 99/100 | 99.0 | 3.749 | 0.100 |

## Paired strategy-space comparisons

- Budget 3: mean V(10)−V(3) = +0.303 live cells; 49/100 sets changed pure-equilibrium existence between at least two action counts.
- Budget 4: mean V(10)−V(3) = +0.510 live cells; 63/100 sets changed pure-equilibrium existence between at least two action counts.
- Budget 5: mean V(10)−V(3) = +0.328 live cells; 61/100 sets changed pure-equilibrium existence between at least two action counts.
- Budget 6: mean V(10)−V(3) = -0.034 live cells; 60/100 sets changed pure-equilibrium existence between at least two action counts.
- Budget 7: mean V(10)−V(3) = +0.520 live cells; 50/100 sets changed pure-equilibrium existence between at least two action counts.

## Interpretation and limitations

An increase in the number of available actions changes the restricted game itself; there is no general monotonicity guarantee for the zero-sum value when both players gain actions.
The absence of a pure equilibrium does not imply the absence of Nash equilibria: every finite game has a mixed equilibrium.
The strategy sets are sampled from restricted non-overlapping 10-cell player regions. These observations do not establish equilibria or universal thresholds for the unrestricted 5×5 automaton.
The sampled game sets are independent within each budget, but the 3/5/10-action outcomes from the same set are paired and should not be treated as independent.
This experiment tests strategy-space scaling, not the effect of changing the board size.

## Reproducibility

Seed: `20261020`. Independent sets per budget: `100`.
Reproduce with `py conway_strategy_scaling.py --samples 100 --seed 20261020`.
All seed patterns, payoff entries, and representative optimal mixed-strategy probabilities are exported as CSV.
