# Phase 5: Nash Equilibrium Robustness and Sensitivity Analysis

## Methods

100 independently sampled restricted 3x3 games were evaluated at each cell budget (3–7 cells per player). Player A selected cells in the top two rows and Player B in the bottom two rows, leaving the central row initially empty. Within each budget and player region, three distinct initial patterns were sampled uniformly without replacement per game. All sampling was reproducible using master seed 20261020. Conway B3/S23 evolved for nine transitions (Generation 1 initial; Generation 10 final).

The primary zero-sum model assigns payoffs (N10, -N10), with minimax mixed strategies computed by linear programming. The secondary model assigns counterfactual marginal-contribution payoffs; pure equilibria were counted, but secondary mixed equilibria were not enumerated.

## Results

| Cells/player | Games | No pure zero-sum NE | Fraction (Wilson 95% CI) | Mean minimax value (95% CI) | Mean secondary pure NE |
|---:|---:|---:|---:|---:|---:|
| 3 | 100 | 12 | 0.120 [0.070, 0.198] | 0.944 [0.617, 1.272] | 3.640 |
| 4 | 100 | 32 | 0.320 [0.237, 0.417] | 2.514 [1.975, 3.054] | 2.330 |
| 5 | 100 | 42 | 0.420 [0.328, 0.518] | 2.280 [1.816, 2.743] | 2.560 |
| 6 | 100 | 38 | 0.380 [0.291, 0.478] | 2.408 [1.917, 2.900] | 2.290 |
| 7 | 100 | 57 | 0.570 [0.472, 0.663] | 3.541 [3.071, 4.011] | 2.030 |

## Interpretation

The analysis quantifies how often the absence of a pure-strategy Nash equilibrium occurs across randomly sampled *restricted* 3x3 strategy sets. A mixed minimax equilibrium exists for every zero-sum finite game, even when pure equilibria exist. Differences across budgets are descriptive and conditional on the specified sampling and spatial-partition protocol.

## Limitations

- The sampled strategy sets are not exhaustive. Results cannot establish a unique critical budget or unrestricted-game equilibrium.
- Each game has three choices per player; the three are sampled configurations, not fixed geometric families.
- The top/bottom partition avoids overlap but may create boundary asymmetry.
- The secondary model does not track persistent cell ownership, and only its pure Nash equilibria are evaluated.
- Confidence intervals describe variation under the chosen random sampling procedure, not uncertainty about deterministic Conway rules.
- The 2,500 density experiments in Phase 3 used a different sampling frame; direct causal comparison is not warranted.

## Reproducibility

Run: `py conway_robustness_analysis.py --samples 100 --seed 20261020`
Outputs include raw strategy boards, all payoff pairings, minimax probabilities, an Excel workbook, CSV files, and five figures.
