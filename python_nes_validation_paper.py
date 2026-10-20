"""NES/Python cross-implementation validation (5 cases x 10 recorded states).

Requires Python 3 only; no third-party packages.
Run on Windows: py python_nes_validation_english.py

Generation 1 is the initial board. Generation 10 follows nine Conway updates.
Outputs a CSV and 50 PNG files grouped into folders by test case.
"""

import csv
import random
import struct
import zlib
from pathlib import Path

BOARD_SIZE = 5
RECORDED_GENERATIONS = 10
RANDOM_SEED = 20261020
OUTPUT_DIRECTORY = Path(__file__).resolve().parent / "NES_Python_Validation_Results"
IMAGE_DIRECTORY = OUTPUT_DIRECTORY / "PNG_States"
CELL_PIXELS = 100
GRID_PIXELS = 3
ALIVE_RGB = (37, 99, 166)
DEAD_RGB = (246, 248, 251)
GRID_RGB = (40, 50, 65)


def board_from_cells(cells):
    return tuple(
        "".join("1" if (row, col) in cells else "0" for col in range(BOARD_SIZE))
        for row in range(BOARD_SIZE)
    )


def random_cells(count, seed):
    generator = random.Random(seed)
    positions = [(row, col) for row in range(BOARD_SIZE) for col in range(BOARD_SIZE)]
    return set(generator.sample(positions, count))


def next_board(board):
    """One synchronous B3/S23 update with dead (non-wrapping) boundaries."""
    updated = []
    for row in range(BOARD_SIZE):
        result_row = ""
        for col in range(BOARD_SIZE):
            neighbors = sum(
                board[r][c] == "1"
                for r in range(max(0, row - 1), min(BOARD_SIZE, row + 2))
                for c in range(max(0, col - 1), min(BOARD_SIZE, col + 2))
                if (r, c) != (row, col)
            )
            alive = board[row][col] == "1"
            result_row += "1" if neighbors == 3 or (alive and neighbors == 2) else "0"
        updated.append(result_row)
    return tuple(updated)


def test_cases():
    return [
        ("C1", "2x2_Block", board_from_cells({(1, 1), (1, 2), (2, 1), (2, 2)}), "Fixed"),
        ("C2", "Three_Cell_Oscillator", board_from_cells({(2, 1), (2, 2), (2, 3)}), "Fixed"),
        ("C3", "Boundary_Pattern", board_from_cells({(0, 0), (0, 1), (0, 2)}), "Fixed"),
        ("C4", "Random_12_Cells", board_from_cells(random_cells(12, RANDOM_SEED)), str(RANDOM_SEED)),
        ("C5", "Random_20_Cells", board_from_cells(random_cells(20, RANDOM_SEED + 1)), str(RANDOM_SEED + 1)),
    ]


def png_chunk(chunk_type, payload):
    data = chunk_type + payload
    return struct.pack("!I", len(payload)) + data + struct.pack("!I", zlib.crc32(data) & 0xffffffff)


def save_board_png(board, filename):
    """Create a publication-friendly PNG with Python's standard library."""
    side = BOARD_SIZE * CELL_PIXELS + (BOARD_SIZE + 1) * GRID_PIXELS
    compressed_rows = bytearray()
    for y in range(side):
        pixel_row = bytearray([0])  # PNG filter type 0
        cell_row = (y - GRID_PIXELS) // (CELL_PIXELS + GRID_PIXELS)
        inside_y = (y >= GRID_PIXELS and (y - GRID_PIXELS) % (CELL_PIXELS + GRID_PIXELS) < CELL_PIXELS)
        for x in range(side):
            cell_col = (x - GRID_PIXELS) // (CELL_PIXELS + GRID_PIXELS)
            inside_x = (x >= GRID_PIXELS and (x - GRID_PIXELS) % (CELL_PIXELS + GRID_PIXELS) < CELL_PIXELS)
            if inside_x and inside_y and 0 <= cell_row < BOARD_SIZE and 0 <= cell_col < BOARD_SIZE:
                rgb = ALIVE_RGB if board[cell_row][cell_col] == "1" else DEAD_RGB
            else:
                rgb = GRID_RGB
            pixel_row.extend(rgb)
        compressed_rows.extend(pixel_row)
    header = b"\x89PNG\r\n\x1a\n"
    ihdr = struct.pack("!2I5B", side, side, 8, 2, 0, 0, 0)
    filename.write_bytes(
        header + png_chunk(b"IHDR", ihdr)
        + png_chunk(b"IDAT", zlib.compress(bytes(compressed_rows), 6))
        + png_chunk(b"IEND", b"")
    )


def main():
    IMAGE_DIRECTORY.mkdir(parents=True, exist_ok=True)
    records = []
    total_images = 0
    for case_id, label, initial_board, seed in test_cases():
        case_folder = IMAGE_DIRECTORY / f"{case_id}_{label}"
        case_folder.mkdir(parents=True, exist_ok=True)
        board = initial_board
        print(f"\n{'=' * 48}\n{case_id} - {label} | Seed: {seed}")
        print("Enter these five rows into the NES as Generation 1 (initial state):")
        print("\n".join(board))
        for generation in range(1, RECORDED_GENERATIONS + 1):
            alive_count = sum(row.count("1") for row in board)
            image_name = f"{case_id}_Generation_{generation:02d}.png"
            relative_path = Path("PNG_States") / case_folder.name / image_name
            save_board_png(board, OUTPUT_DIRECTORY / relative_path)
            records.append([case_id, label.replace("_", " "), seed, generation, alive_count, *board, relative_path.as_posix()])
            total_images += 1
            if generation < RECORDED_GENERATIONS:
                board = next_board(board)

    csv_path = OUTPUT_DIRECTORY / "python_nes_validation_states.csv"
    with csv_path.open("w", newline="", encoding="utf-8-sig") as output_file:
        writer = csv.writer(output_file)
        writer.writerow(["Case", "Configuration", "Seed", "Generation", "Live_Cell_Count",
                         "Row_1", "Row_2", "Row_3", "Row_4", "Row_5", "PNG_File"])
        writer.writerows(records)

    print(f"\nFinished: {len(records)} board states, {total_images} PNG images.")
    print(f"Images: {IMAGE_DIRECTORY}")
    print(f"CSV: {csv_path}")
    print("Generation 1 = initial state; Generation 10 = state after 9 updates.")
    print("To compare NES with Python, use identical initial cell positions.")


if __name__ == "__main__":
    main()
