"""
Experimental Prototype: Strategic Game Based on Conway's Game of Life
----------------------------------------------------------------------
Requirements: Python 3 (Tkinter is usually included).
No external packages are required.

MODEL (provisional; to be validated with the advisor):
- Finite 5x5 board; cells outside the board are considered dead.
- Each player chooses one of three initial configurations.
- The initial configuration is the union of the cells selected by both players.
- The simulation runs for 10 generations using Conway's classic rules.
- Player A's utility: number of living cells at generation 10.
- Player B's utility: the negative of that number (zero-sum game).
- Strategy names and patterns are illustrative examples for this prototype,
  not scientific findings or known optimal strategies.

The program:
1. Displays the initial board and the evolution of the selected combination.
2. Allows the user to advance one generation at a time.
3. Calculates the payoff matrix for all 3x3 combinations.
4. Identifies pure-strategy Nash equilibria, if any.

Important: This is a reproducible prototype for discussing the model.
The code does not, by itself, establish that the model is suitable for publication.
"""

import tkinter as tk
from tkinter import ttk, messagebox

SIZE = 5
HORIZON = 10

# Coordinates (row, column), indexed from 0.
# These are illustrative patterns selected for testing the program.
STRATEGIES = {
    "S1 - 2x2 Block": {(1, 1), (1, 2), (2, 1), (2, 2)},
    "S2 - Horizontal Line of 3": {(2, 1), (2, 2), (2, 3)},
    "S3 - Short Diagonal": {(1, 1), (2, 2), (3, 3)},
}

STRATEGY_NAMES = list(STRATEGIES.keys())


def next_generation(board):
    """Return the next generation on a finite board without periodic boundaries."""
    result = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for r in range(SIZE):
        for c in range(SIZE):
            neighbors = 0

            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    if dr == 0 and dc == 0:
                        continue

                    rr, cc = r + dr, c + dc

                    if 0 <= rr < SIZE and 0 <= cc < SIZE:
                        neighbors += board[rr][cc]

            alive = board[r][c] == 1

            # Conway's Game of Life rules.
            if alive and neighbors in (2, 3):
                result[r][c] = 1
            elif not alive and neighbors == 3:
                result[r][c] = 1

    return result


def initial_board(strategy_a, strategy_b):
    """Combine both players' configurations using set union."""
    cells = STRATEGIES[strategy_a] | STRATEGIES[strategy_b]

    board = [[0 for _ in range(SIZE)] for _ in range(SIZE)]

    for r, c in cells:
        board[r][c] = 1

    return board


def simulate(strategy_a, strategy_b, generations=HORIZON):
    """Simulate the selected strategy combination for a given number of generations."""
    board = initial_board(strategy_a, strategy_b)

    for _ in range(generations):
        board = next_generation(board)

    alive = sum(sum(row) for row in board)

    return alive, board


def matrix_and_equilibria():
    """
    Calculate payoffs (U_A, U_B) and identify pure-strategy Nash equilibria.

    Player A maximizes the number of living cells.
    Player B minimizes the number of living cells.
    """

    payoffs = {}

    # Calculate the payoff for every possible strategy combination.
    for a in STRATEGY_NAMES:
        for b in STRATEGY_NAMES:
            alive, _ = simulate(a, b)
            payoffs[(a, b)] = (alive, -alive)

    # Player A's best responses to each strategy chosen by Player B.
    best_a = {}

    for b in STRATEGY_NAMES:
        maximum = max(
            payoffs[(a, b)][0]
            for a in STRATEGY_NAMES
        )

        best_a[b] = {
            a for a in STRATEGY_NAMES
            if payoffs[(a, b)][0] == maximum
        }

    # Player B's best responses to each strategy chosen by Player A.
    # Since U_B = -U_A, Player B minimizes Player A's payoff.
    best_b = {}

    for a in STRATEGY_NAMES:
        minimum = min(
            payoffs[(a, b)][0]
            for b in STRATEGY_NAMES
        )

        best_b[a] = {
            b for b in STRATEGY_NAMES
            if payoffs[(a, b)][0] == minimum
        }

    # A pure-strategy Nash equilibrium occurs when both players
    # are simultaneously playing a best response to the other.
    equilibria = []

    for a in STRATEGY_NAMES:
        for b in STRATEGY_NAMES:
            if a in best_a[b] and b in best_b[a]:
                equilibria.append(
                    (a, b, payoffs[(a, b)])
                )

    return payoffs, best_a, best_b, equilibria


class LifeGameApp:
    def __init__(self, root):
        self.root = root
        self.root.title(
            "Conway's Game of Life 5x5 - Strategic Game Prototype"
        )
        self.root.minsize(850, 620)

        self.gen = 0
        self.board = None
        self.history = []

        outer = ttk.Frame(root, padding=12)
        outer.pack(fill="both", expand=True)

        ttk.Label(
            outer,
            text=(
                "Provisional Computational Model: "
                "Two Agents on a 5x5 Grid"
            ),
            font=("TkDefaultFont", 13, "bold"),
        ).pack(anchor="w")

        ttk.Label(
            outer,
            text=(
                "Player A maximizes the number of living cells "
                "at generation 10; Player B attempts to minimize it."
            ),
            wraplength=800,
        ).pack(anchor="w", pady=(3, 10))

        # Strategy selection and simulation controls.
        controls = ttk.Frame(outer)
        controls.pack(fill="x", pady=(0, 10))

        self.a_var = tk.StringVar(value=STRATEGY_NAMES[0])
        self.b_var = tk.StringVar(value=STRATEGY_NAMES[1])

        ttk.Label(
            controls,
            text="Player A Strategy:"
        ).grid(row=0, column=0, sticky="w")

        ttk.Combobox(
            controls,
            textvariable=self.a_var,
            values=STRATEGY_NAMES,
            state="readonly",
            width=24,
        ).grid(
            row=0, column=1, padx=(5, 14), sticky="w"
        )

        ttk.Label(
            controls,
            text="Player B Strategy:"
        ).grid(row=0, column=2, sticky="w")

        ttk.Combobox(
            controls,
            textvariable=self.b_var,
            values=STRATEGY_NAMES,
            state="readonly",
            width=24,
        ).grid(
            row=0, column=3, padx=5, sticky="w"
        )

        ttk.Button(
            controls,
            text="Simulate Combination",
            command=self.start_simulation,
        ).grid(row=0, column=4, padx=(12, 4))

        ttk.Button(
            controls,
            text="Next Generation",
            command=self.step,
        ).grid(row=0, column=5, padx=4)

        # Main content area.
        content = ttk.Frame(outer)
        content.pack(fill="both", expand=True)

        left = ttk.Frame(content)
        left.pack(side="left", fill="y", padx=(0, 20))

        self.board_canvas = tk.Canvas(
            left,
            width=310,
            height=310,
            background="white",
            highlightthickness=1,
            highlightbackground="#888",
        )
        self.board_canvas.pack()

        self.status = ttk.Label(
            left,
            text="Select the strategies and click Simulate."
        )
        self.status.pack(anchor="w", pady=8)

        ttk.Label(
            left,
            text="Legend:"
        ).pack(anchor="w")

        ttk.Label(
            left,
            text="■ Living cell    □ Dead cell"
        ).pack(anchor="w")

        # Payoff matrix and Nash equilibrium results.
        right = ttk.Frame(content)
        right.pack(side="left", fill="both", expand=True)

        ttk.Label(
            right,
            text="Payoff Matrix (U_A, U_B)",
            font=("TkDefaultFont", 11, "bold"),
        ).pack(anchor="w")

        ttk.Button(
            right,
            text="Calculate Payoff Matrix and Equilibria",
            command=self.show_matrix,
        ).pack(anchor="w", pady=(5, 5))

        self.matrix_text = tk.Text(
            right,
            width=62,
            height=20,
            wrap="word",
            font=("TkFixedFont", 9),
        )
        self.matrix_text.pack(fill="both", expand=True)

        self.matrix_text.insert(
            "1.0",
            (
                "Click 'Calculate Payoff Matrix and Equilibria' "
                "to evaluate all 9 strategy combinations.\n"
            ),
        )

        # Explicitly document the assumptions requiring validation.
        disclaimer = (
            "Assumptions to be agreed upon with the advisor: "
            "utility function, strategies, union of placements, "
            "boundary conditions, and the 10-generation horizon."
        )

        ttk.Label(
            outer,
            text=disclaimer,
            wraplength=820,
            foreground="#444",
        ).pack(anchor="w", pady=(10, 0))

        self.start_simulation()

    def draw_board(self):
        """Render the current board and generation number."""
        self.board_canvas.delete("all")

        margin, cell = 25, 52

        for r in range(SIZE):
            for c in range(SIZE):
                x1 = margin + c * cell
                y1 = margin + r * cell
                x2 = x1 + cell - 3
                y2 = y1 + cell - 3

                alive = self.board[r][c] == 1
                fill = "#222222" if alive else "#FFFFFF"

                self.board_canvas.create_rectangle(
                    x1,
                    y1,
                    x2,
                    y2,
                    fill=fill,
                    outline="#777777",
                    width=1,
                )

        self.board_canvas.create_text(
            155,
            12,
            text=f"Generation {self.gen}",
            font=("TkDefaultFont", 10, "bold"),
        )

    def start_simulation(self):
        """Initialize the board using the currently selected strategies."""
        self.gen = 0

        self.board = initial_board(
            self.a_var.get(),
            self.b_var.get(),
        )

        self.history = [self.board]

        self.draw_board()

        alive = sum(sum(row) for row in self.board)

        self.status.config(
            text=f"Generation 0: {alive} living cells."
        )

    def step(self):
        """Advance the simulation by one generation."""
        if self.board is None:
            self.start_simulation()

        if self.gen >= HORIZON:
            messagebox.showinfo(
                "Simulation Complete",
                f"Generation {HORIZON} has already been reached.",
            )
            return

        self.board = next_generation(self.board)
        self.gen += 1
        self.history.append(self.board)

        self.draw_board()

        alive = sum(sum(row) for row in self.board)

        self.status.config(
            text=f"Generation {self.gen}: {alive} living cells."
        )

        if self.gen == HORIZON:
            self.status.config(
                text=(
                    f"Final result: {alive} living cells "
                    f"at generation {HORIZON}."
                )
            )

    def show_matrix(self):
        """Calculate and display the payoff matrix and pure Nash equilibria."""
        payoffs, best_a, best_b, equilibria = matrix_and_equilibria()

        lines = []

        lines.append(
            "Each cell contains (U_A, U_B), where U_A = N10 and U_B = -N10.\n"
        )

        lines.append(
            "Rows represent Player A's strategy; "
            "columns represent Player B's strategy.\n"
        )

        col_width = 22

        lines.append(
            "A \\ B".ljust(24)
            + "".join(
                f"{('B' + str(i + 1)):>{col_width}}"
                for i in range(3)
            )
        )

        for i, a in enumerate(STRATEGY_NAMES):
            row = f"A{i + 1}: {a}".ljust(24)

            for b in STRATEGY_NAMES:
                ua, ub = payoffs[(a, b)]

                row += (
                    f"{(str(ua) + ', ' + str(ub)):>{col_width}}"
                )

            lines.append(row)

        lines.append(
            "\nPlayer A's best responses (maximizes U_A), given Player B:"
        )

        for b in STRATEGY_NAMES:
            idx = STRATEGY_NAMES.index(b) + 1

            answers = [
                f"A{STRATEGY_NAMES.index(a) + 1}"
                for a in sorted(
                    best_a[b],
                    key=STRATEGY_NAMES.index,
                )
            ]

            lines.append(
                f"  If Player B chooses B{idx}: {', '.join(answers)}"
            )

        lines.append(
            "\nPlayer B's best responses (maximizes U_B = -N10), "
            "given Player A:"
        )

        for a in STRATEGY_NAMES:
            idx = STRATEGY_NAMES.index(a) + 1

            answers = [
                f"B{STRATEGY_NAMES.index(b) + 1}"
                for b in sorted(
                    best_b[a],
                    key=STRATEGY_NAMES.index,
                )
            ]

            lines.append(
                f"  If Player A chooses A{idx}: {', '.join(answers)}"
            )

        lines.append(
            "\nPure-Strategy Nash Equilibria:"
        )

        if equilibria:
            for a, b, payoff in equilibria:
                lines.append(
                    f"  ({a}, {b}) -> Payoffs {payoff}; "
                    f"A{STRATEGY_NAMES.index(a) + 1} "
                    f"against B{STRATEGY_NAMES.index(b) + 1}"
                )
        else:
            lines.append(
                "  No pure-strategy Nash equilibrium was found "
                "among these 9 combinations."
            )

            lines.append(
                "  This does not rule out an equilibrium in mixed strategies."
            )

        lines.append(
            "\nNOTE: The results depend on the illustrative strategies "
            "and the assumptions of the model. "
            "They do not constitute a scientific conclusion by themselves."
        )

        self.matrix_text.delete("1.0", "end")
        self.matrix_text.insert("1.0", "\n".join(lines))


def main():
    """Initialize and run the graphical application."""
    root = tk.Tk()

    try:
        style = ttk.Style()

        if "vista" in style.theme_names():
            style.theme_use("vista")

    except tk.TclError:
        pass

    LifeGameApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()