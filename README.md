# Conway's Game of Life: Computational Experiments, Game Theory, and Nash Equilibrium Analysis

A collection of reproducible Python experiments investigating **Conway's Game of Life on a finite 5 × 5 grid**, from cellular-automaton validation and population persistence to **two-player strategic interactions, Nash equilibria, robustness, spatial sensitivity, strategy-space scaling, and randomization controls**.

The repository contains an interactive demonstration as well as independent computational research scripts. The experiments use Conway's classical **B3/S23** transition rule; competitive behavior arises from the *chosen payoff functions*, not from a modification of the cellular automaton.

> **Research status:** Experimental computational models. Reported equilibria refer to the finite, restricted strategy sets constructed by each script; they do **not** establish equilibria over every possible configuration of the 5 × 5 board. The underlying NES measurements used for historical comparisons are aggregate reference values, not a complete raw NES dataset.

## Contents

1. [Research objectives](#research-objectives)
2. [Cellular automaton and experimental conventions](#cellular-automaton-and-experimental-conventions)
3. [Programs and research workflow](#programs-and-research-workflow)
4. [Installation](#installation)
5. [Running the experiments](#running-the-experiments)
6. [Game-theoretic models](#game-theoretic-models)
7. [Outputs and reproducibility](#outputs-and-reproducibility)
8. [Limitations](#limitations)
9. [Future research](#future-research)
10. [Author and citation](#author-and-citation)

## Research objectives

- Validate and reproduce finite-grid Conway trajectories, including fixed reference configurations and freshly sampled states.
- Characterize the effect of initial live-cell density on persistence, survival, final population, and observed dynamical behavior.
- Construct finite two-player games in which each player chooses an initial cell arrangement.
- Evaluate **pure-strategy Nash equilibria**, **mixed-strategy equilibria**, and **minimax values** under explicitly defined utilities.
- Test the dependence of strategic outcomes on the selected strategy families, cell budgets, spatial transformations, and number of available actions.
- Compare structured Conway payoff matrices with permutation-based controls.
- Export auditable datasets, plots, and reports for subsequent scientific analysis.

## Cellular automaton and experimental conventions

Most batch experiments share the following underlying model:

| Property | Definition |
| --- | --- |
| Grid | Finite 5 × 5 board (25 cells) |
| Update | Synchronous Conway B3/S23 |
| Birth | A dead cell becomes alive with exactly 3 living neighbors |
| Survival | A living cell survives with 2 or 3 living neighbors |
| Boundary | Cells outside the board are permanently dead; no wraparound |
| State encoding | Five binary rows, often separated by `/` in CSV outputs |
| Batch observation horizon | **Generation 1 = initial state; Generation 10 = state after 9 updates** |
| Game outcome | Commonly, the number of live cells in the last observed state, denoted `N10` |

**Important horizon difference:** `conway_nash_3x3.py` uses `HORIZON = 10` and applies **10 updates** inside its `simulate()` function. The other major batch studies typically record **10 states including the initial state**, hence **9 updates**. Results from the interactive prototype and later batch studies should not be interpreted as using identical horizons without adjustment.

### Density and persistence

In the extended density study, an initial population of 1 through 25 live cells is sampled uniformly from the grid positions at each fixed count, using 100 trials per count. **Persistence** is the number of observed nonempty states among Generations 1–10, not necessarily the final number of live cells. Terminal trajectories are operationally classified as **Extinct**, **Stable**, **Oscillatory**, or **Dynamic** within the finite observation window.

## Programs and research workflow

| Script | Role | Main output / capability |
| --- | --- | --- |
| `conway_nash_3x3.py` | Interactive original game-theory prototype | Tkinter board, 3 × 3 payoff matrix, pure Nash equilibria |
| `python_nes_validation_dual_mode.py` | Python/NES reference-case generation | Fixed reference and fresh-random trajectories, PNG states, CSV |
| `conway_extended_experiments.py` | Extended population-density experiment | 2,500 runs, 25,000 recorded states, CSV, Excel, figures |
| `analyze_conway_results.py` | Density dataset auditing and statistical reporting | Audits, summary tables, Excel, figures, Markdown/text report |
| `conway_game_theory_strategy_analysis.py` | Phase 4: deterministic strategy families | Restricted zero-sum and non-zero-sum 3 × 3 games; pure/mixed analyses |
| `conway_robustness_analysis.py` | Phase 5: sampled-game robustness | Across-sample equilibrium statistics, minimax analysis, figures |
| `conway_spatial_sensitivity.py` | Phase 6: spatial sensitivity | Paired transformations and equilibrium-status comparisons |
| `conway_strategy_scaling.py` | Phase 7: strategy-space scaling | Nested 3 × 3, 5 × 5, and 10 × 10 payoff matrices |
| `conway_randomization.py` | Phase 8: permutation baseline | Payoff-shuffle controls and paired differences |

The phase labels reflect those recorded in the scripts. The NES validation, density, and interactive programs are separate research components rather than interchangeable phases of the same game.

### 1. Interactive prototype — `conway_nash_3x3.py`

A Tkinter interface in which two players independently choose among three illustrative patterns:

- **S1:** 2 × 2 block.
- **S2:** horizontal three-cell line.
- **S3:** short diagonal of three cells.

The initial board is the **set union** of both selections; overlapping cells are counted only once. The program advances the board interactively, computes all nine payoff pairs, identifies each player's best responses, and reports **pure-strategy Nash equilibria**, if any. It is a **zero-sum** game with payoffs `(N, −N)`. The patterns are examples rather than proven optimal strategies. This specific GUI does **not** solve mixed equilibria.

### 2. NES/Python trajectory references — `python_nes_validation_dual_mode.py`

Generates documented Python trajectories for five reference cases: a 2 × 2 block, a three-cell oscillator, a boundary pattern, and two fixed-seed random boards containing 12 and 20 live cells. The fixed-reference outputs are created only when absent so existing reference evidence is not overwritten. Each additional execution creates **new random 12- and 20-cell cases** with recorded seeds in a unique run directory.

Produces per-generation **PNG images** and a `python_nes_validation_states.csv` file for each group of cases. The script reproduces Python trajectories for the named reference cases; **direct equivalence with physical NES execution requires separately supplied NES measurements or traces**.

### 3. Extended density study — `conway_extended_experiments.py`

Runs **100 initial configurations for each live-cell count from 1 to 25**, resulting in **2,500 trials** and **25,000 recorded states** (10 per trial). Tracks persistence, Generation-10 survival, terminal population, and terminal behavior classes. Uses a fixed master seed (`20261020`) and derives a distinct deterministic seed for each density/trial pair.

The study includes a comparison with previously reported **historical NES mean-persistence values** (10 trials per density). Those aggregate numbers are embedded as a reference series; the underlying raw NES trials are **not reconstructed** by the script. Results include CSV data, an Excel workbook, plots, and JSON metadata.

### 4. Audit and statistical analysis — `analyze_conway_results.py`

Reads the three principal CSVs generated by the extended density study, including data stored inside an accepted study ZIP. Rechecks board encodings, live-cell totals, recorded transitions, run identifiers, persistence, terminal classifications, and expected record counts. Creates additional statistical summaries, figures, an Excel workbook, and reports (`statistical_report.md` and `.txt`).

**Run this after generating the extended density dataset.** The audit tests consistency of recorded data against the implemented definitions; it does not independently validate the scientific interpretation of historical NES measurements.

### 5. Phase 4 — deterministic game-theoretic analysis — `conway_game_theory_strategy_analysis.py`

Constructs restricted **3 × 3 games** for cell budgets of **3, 4, 5, and 6 cells per player**. Each player receives three algorithmically chosen strategy families: **Compact**, **Row-oriented**, and **Dispersed**. Player A's initial placements occupy rows 0–1 and Player B's occupy rows 3–4, with the central row initially empty. Strategies cannot overlap initially, but subsequent Conway births may bridge the regions.

The script compares **two distinct utility models**: zero-sum survival-versus-extinction, and a non-zero-sum counterfactual mutual-preservation model. It calculates payoff matrices, pure equilibria, a zero-sum minimax solution using linear programming, and feasible representatives of non-zero-sum mixed equilibria by support enumeration. Exports seven CSV files, Excel, figures, metadata, and a scientific report.

### 6. Phase 5 — robustness — `conway_robustness_analysis.py`

Samples independent restricted **3 × 3** strategy games across budgets of **3–7 cells per player** (default: **100 sampled games per budget**). Studies how the existence of pure equilibria and zero-sum minimax values vary across sampled strategy sets; also reports a secondary counterfactual-preservation analysis. The code computes descriptive confidence intervals and generates CSV, Excel, charts, and a scientific report. Results apply to the sampling and placement design, not to an unrestricted game.

### 7. Phase 6 — spatial sensitivity — `conway_spatial_sensitivity.py`

Applies four possible within-region transformations—**identity**, **horizontal reflection**, **one-column cyclic shift**, and **row swap**—to each player's patterns, giving **16 paired transformation combinations** per underlying sampled strategy set. Budgets are **3–7 cells per player**; default is **40 independently sampled strategy sets per budget**.

Measures changes in pure-equilibrium existence and minimax value. The transformations are bijections within each player's initial placement region, **not generally symmetries of Conway's complete board**. The 16 transformed observations from any one sample are therefore dependent, and should not be presented as independent random games.

### 8. Phase 7 — strategy-space scaling — `conway_strategy_scaling.py`

Tests whether results change when players have **3, 5, or 10 available actions**, holding the sampled initial strategy sets nested: the same sampled ten actions produce the first-three, first-five, and all-ten action comparisons. Each budget (**3–7 cells per player**) has **100 sampled strategy sets by default**. Generates full payoff tables, mixed minimax policies, pure-equilibrium indicators, CSV data, visualizations, and an English report.

This is scaling of the **restricted action set on the same 5 × 5 board**, not an increase in board dimensions. The program writes to `Conway_Strategy_Scaling/` by default.

### 9. Phase 8 — payoff-permutation controls — `conway_randomization.py`

Reads **`games.csv` and `payoffs.csv` from Phase 7**, then repeatedly shuffles the entries of each payoff matrix while preserving its multiset of payoffs. It compares the observed absence of pure Nash equilibria with a matrix-permutation baseline. Default settings use **200 payoff permutations per game**; the first **12** are also used for a minimax-value comparison.

The script reports game-level paired differences, aggregated comparisons by budget and action count, bootstrap intervals, an approximate Monte Carlo randomization comparison, figures, and a scientific report. This permutation test is a **control for payoff arrangement**, not a claim that shuffled matrices arise naturally from Conway dynamics.

## Installation

Install **Python 3.9 or newer** as a practical starting point (the scripts have not been verified here against every Python version). Clone the repository:

```bash
git clone https://github.com/Bsenzio/conway-life-game-theory.git
cd conway-life-game-theory
```

Create a virtual environment (recommended):

```bash
python -m venv .venv
```

On Windows:

```powershell
.venv\Scripts\activate
```

On macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies for the computational studies:

```bash
python -m pip install numpy scipy matplotlib openpyxl
```

- **Standard library only:** `python_nes_validation_dual_mode(2).py`.
- **Tkinter standard-library GUI:** `conway_nash_3x3.py` (Tkinter may require a separate system package on Linux).
- **Matplotlib + openpyxl:** extended density experiment and its audit script.
- **NumPy + SciPy + Matplotlib (+ openpyxl where applicable):** game-theory research scripts.

No NES emulator or original NES hardware is required to run the supplied Python code.

## Running the experiments

The commands below use the **exact uploaded filenames**. The parentheses in some filenames require quotation marks in a shell. If you rename files before uploading to GitHub, update these commands accordingly.

**Interactive original prototype:**

```bash
python conway_nash_3x3.py
```

**Generate Python/NES reference and fresh-random trajectories:**

```bash
python "python_nes_validation_dual_mode(2).py"
```

**Generate extended density data, then audit/analyze it:**

```bash
python "conway_extended_experiments(1).py"
python "analyze_conway_results(1).py" --input Conway_Extended_Study
```

**Phase 4 — deterministic strategy families:**

```bash
python conway_game_theory_strategy_analysis.py
```

**Phase 5 — robustness:**

```bash
python "conway_robustness_analysis(2).py" --samples 100 --seed 20261020
```

**Phase 6 — spatial sensitivity:**

```bash
python "conway_spatial_sensitivity(2).py" --samples 40 --seed 20261020
```

**Phase 7 — strategy scaling:**

```bash
python "conway_strategy_scaling(2).py" --samples 100 --seed 20261020
```

**Phase 8 — payoff permutation baseline (run Phase 7 first):**

```bash
python conway_randomization.py --input-dir Conway_Strategy_Scaling --output-dir Conway_Phase8 --permutations 200 --value-permutations 12 --seed 20261020
```

For parameter details, use `--help` with scripts that support command-line options. **Phase 8 requires the output tables produced by Phase 7**; the audit script likewise requires the extended density study's output files.

## Game-theoretic models

Let `s_A` and `s_B` be the strategies selected by players A and B, respectively, and let `N10(s_A ∪ s_B)` be the number of living cells in the final observed state after the chosen initial patterns are combined.

### Model 1: zero-sum survival versus extinction

The primary game-theoretic studies define:

\[
u_A(s_A,s_B)=N_{10}(s_A\cup s_B)
\]

\[
u_B(s_A,s_B)=-N_{10}(s_A\cup s_B)
\]

Player A **maximizes** the final population; Player B **minimizes** it. If `M` is Player A's payoff matrix, a pure saddle point exists at `(i,j)` when its entry is maximal in its column and minimal in its row:

\[
M_{ij}=\max_{r}M_{rj}=\min_{c}M_{ic}.
\]

Even if no pure equilibrium exists, a finite zero-sum game has a mixed-strategy minimax solution. Several batch scripts compute such solutions via linear programming.

### Model 2: counterfactual mutual preservation

Phase 4 and related secondary analyses consider each player's **marginal contribution** to the final population relative to the opponent acting alone:

\[
u_A(s_A,s_B)=N_{10}(s_A\cup s_B)-N_{10}(s_B)
\]

\[
u_B(s_A,s_B)=N_{10}(s_A\cup s_B)-N_{10}(s_A).
\]

This is generally a **non-zero-sum** game. These utilities do **not** imply that cells are tagged by owner or that distinct species compete under different cellular-automaton rules. Equilibrium algorithms and reported results depend on the model; a zero-sum minimax value is not interchangeable with a non-zero-sum equilibrium payoff.

### Restricted strategies and equilibrium interpretation

In the phase-based studies, the full board is **not** searched exhaustively over all player actions. Instead, the scripts construct or sample finite strategy menus within designated placement regions. A Nash equilibrium is therefore an equilibrium **relative to the available actions in that specific experiment**. In degenerate non-zero-sum games, support enumeration may return a feasible representative without enumerating an entire continuum of equilibria.

## Outputs and reproducibility

Each experiment creates its own output folder; generated data and figures are generally placed beside the scripts or under the current working directory, depending on the implementation.

| Experiment | Default output folder |
| --- | --- |
| NES/Python reference | `NES_Python_Validation_Results/` |
| Extended density | `Conway_Extended_Study/` |
| Density audit and statistics | `Conway_Statistical_Analysis/` (normally adjacent to the dataset) |
| Phase 4 | `Conway_Game_Theory_Results/` |
| Phase 5 | `Conway_Robustness_Analysis/` |
| Phase 6 | `Conway_Spatial_Sensitivity/` |
| Phase 7 | `Conway_Strategy_Scaling/` |
| Phase 8 | `Conway_Phase8/` |

Common exported materials include **CSV** tables of strategy choices, payoffs, and/or simulation states; **PNG** figures; **JSON** metadata; **Excel workbooks** in studies that use `openpyxl`; and human-readable **Markdown scientific reports**. The interactive Tkinter prototype primarily displays results on screen.

**Reproducibility practices:**

- Batch scripts document seeds (commonly `20261020`) and, where appropriate, permit `--seed` and `--samples` to be overridden.
- The extended density experiment derives deterministic seeds from density and trial identifiers.
- Fixed NES/Python reference cases remain separate from fresh random cases; fresh-case seeds are recorded with the outputs.
- Phase 7 uses nested action sets for paired comparisons across 3, 5, and 10 strategies.
- Phase 8 uses Phase 7's saved game and payoff tables as its input and preserves each matrix's payoff values under permutation.
- Statistical summaries and charts are **outputs produced when scripts are run**; this README does not assert numerical findings that have not been independently checked against generated results.

### Repository layout

The following lists the **nine Python source files supplied for this README**; generated output directories appear after their corresponding scripts are executed:

```text
conway-life-game-theory/
├── README.md
├── conway_nash_3x3.py
├── python_nes_validation_dual_mode(2).py
├── conway_extended_experiments(1).py
├── analyze_conway_results(1).py
├── conway_game_theory_strategy_analysis.py
├── conway_robustness_analysis(2).py
├── conway_spatial_sensitivity(2).py
├── conway_strategy_scaling(2).py
└── conway_randomization.py
```

*Note:* This tree describes the provided files, not a verification that all filenames already appear in the public GitHub repository. Retain any existing `.gitignore`, license, or additional files when updating the repository.

## Limitations

1. **Restricted games:** Game-theoretic equilibria apply only to the tested strategy sets and payoff definitions. None of the included scripts proves an equilibrium over the complete unrestricted board-strategy space.
2. **Finite grid:** A 5 × 5 board with dead exterior boundaries has strong edge and location effects; results need not generalize to larger boards or periodic boundaries.
3. **Different horizons:** The GUI prototype performs ten updates, while the later batch studies normally use nine updates to reach the state labeled Generation 10.
4. **Designed utilities:** Survival-versus-extinction and mutual-preservation rewards are external modeling decisions, not rules inherent in Conway's Game of Life.
5. **Sampling constraints:** Cell budget, placement regions, candidate-pattern selection, and finite sample counts all condition the observed distributions.
6. **Historical NES data:** The density-study comparison includes previously reported NES **aggregate means**, not all original trial-level trajectories; Python generation of reference patterns does not by itself verify machine-level equivalence.
7. **Statistical interpretation:** Intervals and randomization procedures use stated approximations and sampling designs; paired or transformed observations should not be treated as independent where they are not.
8. **Finite observation:** Labels such as *Dynamic* describe the observed horizon, not an infinite-time proof of non-recurrence.

## Future research

Possible next steps include standardized generation indexing across all scripts; additional payoff and survival objectives; systematic comparisons across larger grids and alternative boundaries; expanded action-selection mechanisms; full mixed-equilibrium and degeneracy analysis for additional non-zero-sum models; independent NES-versus-Python trace comparison using raw hardware/emulator logs; and further paired sensitivity analyses with documented uncertainty.

## Author and citation

**Bruno Senzio-Savino** — [@Bsenzio](https://github.com/Bsenzio)

Repository: <https://github.com/Bsenzio/conway-life-game-theory>

If you use this code in research or teaching, please cite the repository URL and the specific commit or release used. A formal paper citation, DOI, and software license should be added here **only when their final details are available**.

---

**Disclaimer:** This repository provides reproducible computational tools and exploratory models. Its outputs should be evaluated in the context of the exact code version, assumptions, parameter choices, and generated datasets used for each experiment.
