# Phase 8 — Structural equilibrium analysis against payoff-permutation baselines

Input: Phase 7; 1500 sampled games, 200 permutations/game (300,000 shuffled matrices).

Each permutation preserves the exact payoff multiset of its original matrix, including all ties, but destroys its row/column strategic arrangement. The 5×5 Conway board and B3/S23 rules are unchanged.

## Results

| Cells/player | Strategies | Conway no-pure % | Shuffled no-pure % | Difference (pp) | Paired bootstrap 95% CI (pp) | Exploratory p |
|---:|---:|---:|---:|---:|---:|---:|
| 3 | 3×3 | 15.0 | 26.8 | -11.8 | [-18.1, -5.4] | 0.0017 |
| 3 | 5×5 | 31.0 | 43.8 | -12.8 | [-20.5, -5.3] | 0.0013 |
| 3 | 10×10 | 51.0 | 75.1 | -24.1 | [-32.6, -15.8] | 0.0000 |
| 4 | 3×3 | 36.0 | 43.4 | -7.4 | [-16.4, +1.6] | 0.1167 |
| 4 | 5×5 | 74.0 | 79.8 | -5.8 | [-14.7, +2.7] | 0.1305 |
| 4 | 10×10 | 96.0 | 99.2 | -3.2 | [-7.2, -0.0] | 0.0098 |
| 5 | 3×3 | 39.0 | 44.4 | -5.4 | [-14.7, +3.7] | 0.2573 |
| 5 | 5×5 | 74.0 | 74.9 | -0.9 | [-8.8, +6.5] | 0.8954 |
| 5 | 10×10 | 94.0 | 96.7 | -2.7 | [-7.4, +1.3] | 0.1416 |
| 6 | 3×3 | 42.0 | 49.7 | -7.7 | [-16.0, +0.7] | 0.0979 |
| 6 | 5×5 | 72.0 | 83.4 | -11.4 | [-18.8, -4.2] | 0.0013 |
| 6 | 10×10 | 94.0 | 99.0 | -5.0 | [-10.0, -0.9] | 0.0003 |
| 7 | 3×3 | 53.0 | 53.1 | -0.1 | [-8.9, +9.1] | 1.0000 |
| 7 | 5×5 | 85.0 | 86.2 | -1.2 | [-8.2, +5.1] | 0.7615 |
| 7 | 10×10 | 99.0 | 99.6 | -0.6 | [-2.7, +0.5] | 0.3046 |

## Interpretation

A difference from this baseline establishes nonrandom strategic arrangement relative to uniform within-matrix permutations; it does **not** uniquely identify Conway dynamics as the cause, because spatially restricted seeding and shared-action correlations also shape the matrix.

The permutation null treats each matrix payoff multiset as fixed. The per-game control rate is estimated by Monte Carlo. The paired confidence interval resamples games (not individual permutations). Exploratory p-values approximate a conditional null using Monte Carlo-estimated game-specific Bernoulli probabilities and are not corrected for multiple comparisons.

Minimax control values are computed on a smaller subset of permutations per game; they are descriptive, not formal tests.

Strategy sets of sizes 3, 5, and 10 are nested within the same 10-action samples, so comparisons across sizes are correlated. No claims of universal behavior or hardware execution of these randomized controls are made.

## Reproducibility

`py -m pip install numpy scipy matplotlib`

`py conway_phase8_randomization.py --input-dir Conway_Strategy_Scaling --output-dir Conway_Phase8 --permutations 200 --value-permutations 12 --seed 20261020`
