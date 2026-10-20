"""NES/Python validation with immutable paper references and fresh random trials.

Python 3 standard library only.
Run: py python_nes_validation_dual_mode.py

Generation 1 = initial state; Generation 10 = after nine Conway updates.
Reference cases C4/C5 use the original paper seeds on every run.
Fresh cases R4/R5 use new recorded seeds on every run.
"""
import csv
import random
import secrets
import struct
import zlib
from datetime import datetime
from pathlib import Path

BOARD_SIZE = 5
RECORDED_GENERATIONS = 10
REFERENCE_SEEDS = {"C4": 20261020, "C5": 20261021}
ROOT = Path(__file__).resolve().parent / "NES_Python_Validation_Results"
REFERENCE_ROOT = ROOT / "Paper_Reference"
RANDOM_ROOT = ROOT / "New_Random_Experiments"
CELL_PIXELS = 100
GRID_PIXELS = 3
ALIVE_RGB = (37, 99, 166)
DEAD_RGB = (246, 248, 251)
GRID_RGB = (40, 50, 65)


def board_from_cells(cells):
    return tuple("".join("1" if (r, c) in cells else "0" for c in range(BOARD_SIZE)) for r in range(BOARD_SIZE))


def random_board(count, seed):
    rng = random.Random(seed)
    positions = [(r, c) for r in range(BOARD_SIZE) for c in range(BOARD_SIZE)]
    return board_from_cells(set(rng.sample(positions, count)))


def next_board(board):
    """Synchronous Conway B3/S23, finite grid with dead exterior."""
    updated = []
    for r in range(BOARD_SIZE):
        line = ""
        for c in range(BOARD_SIZE):
            neighbors = sum(board[rr][cc] == "1"
                            for rr in range(max(0, r - 1), min(BOARD_SIZE, r + 2))
                            for cc in range(max(0, c - 1), min(BOARD_SIZE, c + 2))
                            if (rr, cc) != (r, c))
            alive = board[r][c] == "1"
            line += "1" if neighbors == 3 or (alive and neighbors == 2) else "0"
        updated.append(line)
    return tuple(updated)


def png_chunk(chunk_type, payload):
    data = chunk_type + payload
    return struct.pack("!I", len(payload)) + data + struct.pack("!I", zlib.crc32(data) & 0xffffffff)


def save_board_png(board, filename):
    """Save a grid image using only the Python standard library."""
    side = BOARD_SIZE * CELL_PIXELS + (BOARD_SIZE + 1) * GRID_PIXELS
    pixel_data = bytearray()
    for y in range(side):
        row_data = bytearray([0])
        r = (y - GRID_PIXELS) // (CELL_PIXELS + GRID_PIXELS)
        inside_y = y >= GRID_PIXELS and (y - GRID_PIXELS) % (CELL_PIXELS + GRID_PIXELS) < CELL_PIXELS
        for x in range(side):
            c = (x - GRID_PIXELS) // (CELL_PIXELS + GRID_PIXELS)
            inside_x = x >= GRID_PIXELS and (x - GRID_PIXELS) % (CELL_PIXELS + GRID_PIXELS) < CELL_PIXELS
            rgb = (ALIVE_RGB if board[r][c] == "1" else DEAD_RGB) if (inside_x and inside_y and 0 <= r < BOARD_SIZE and 0 <= c < BOARD_SIZE) else GRID_RGB
            row_data.extend(rgb)
        pixel_data.extend(row_data)
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack("!2I5B", side, side, 8, 2, 0, 0, 0)
    filename.write_bytes(header + png_chunk(b"IHDR", ihdr) + png_chunk(b"IDAT", zlib.compress(bytes(pixel_data), 6)) + png_chunk(b"IEND", b""))


def reference_cases():
    return [
        ("C1", "2x2_Block", board_from_cells({(1, 1), (1, 2), (2, 1), (2, 2)}), "Fixed"),
        ("C2", "Three_Cell_Oscillator", board_from_cells({(2, 1), (2, 2), (2, 3)}), "Fixed"),
        ("C3", "Boundary_Pattern", board_from_cells({(0, 0), (0, 1), (0, 2)}), "Fixed"),
        ("C4", "Random_12_Cells", random_board(12, REFERENCE_SEEDS["C4"]), str(REFERENCE_SEEDS["C4"])),
        ("C5", "Random_20_Cells", random_board(20, REFERENCE_SEEDS["C5"]), str(REFERENCE_SEEDS["C5"])),
    ]


def write_experiment(folder, cases):
    folder.mkdir(parents=True, exist_ok=False)
    rows = []
    for case_id, label, initial_board, seed in cases:
        image_folder = folder / "PNG_States" / f"{case_id}_{label}"
        image_folder.mkdir(parents=True)
        print(f"\n{case_id}: {label} | Seed: {seed}\nInitial board (Generation 1):")
        print("\n".join(initial_board))
        board = initial_board
        for generation in range(1, RECORDED_GENERATIONS + 1):
            name = f"{case_id}_Generation_{generation:02d}.png"
            save_board_png(board, image_folder / name)
            rows.append([case_id, label.replace("_", " "), seed, generation,
                         sum(r.count("1") for r in board), *board,
                         (Path("PNG_States") / image_folder.name / name).as_posix()])
            if generation < RECORDED_GENERATIONS:
                board = next_board(board)
    with (folder / "python_nes_validation_states.csv").open("w", newline="", encoding="utf-8-sig") as stream:
        writer = csv.writer(stream)
        writer.writerow(["Case", "Configuration", "Seed", "Generation", "Live_Cell_Count",
                         "Row_1", "Row_2", "Row_3", "Row_4", "Row_5", "PNG_File"])
        writer.writerows(rows)
    print(f"\nSaved {len(rows)} PNGs and CSV in: {folder}")


def main():
    # Reference output is written only if absent: never overwrite the paper evidence.
    if REFERENCE_ROOT.exists():
        print(f"Paper reference already exists; keeping it unchanged: {REFERENCE_ROOT}")
    else:
        write_experiment(REFERENCE_ROOT, reference_cases())

    # Unique random seeds and a unique run folder allow full reproducibility.
    seed12 = secrets.randbits(64)
    seed20 = secrets.randbits(64)
    run_id = datetime.now().strftime("%Y%m%d_%H%M%S_%f") + f"_{secrets.token_hex(3)}"
    run_folder = RANDOM_ROOT / f"Run_{run_id}"
    write_experiment(run_folder, [
        ("R4", "Random_12_Cells", random_board(12, seed12), str(seed12)),
        ("R5", "Random_20_Cells", random_board(20, seed20), str(seed20)),
    ])
    print("\nReference C4/C5 remain fixed; new R4/R5 are random and reproducible from their saved seeds.")
    print("Generation 1 = initial state; Generation 10 = nine transitions.")


if __name__ == "__main__":
    main()
