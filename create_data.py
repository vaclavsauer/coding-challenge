import argparse
import random
import string
import logging
from io import TextIOWrapper

logging.basicConfig()
logging.getLogger().setLevel(logging.INFO)

CHARS = " " + string.ascii_letters

"""
Simple command line tool to generate large files
"""


def write_lines(file: TextIOWrapper, lines_count: int) -> None:
    for line_number in range(1, lines_count + 1):
        # Get line length using exponential random number to reduce file size
        line_length = min(1000, int(random.expovariate(lambd=1.0) * 100))

        # Construct line
        line = ""
        for _ in range(0, line_length):
            line += random.choice(CHARS)

        file.write(line + "\n")

        # Print progress
        if line_number % min(10000, lines_count) == 0:
            logging.info(f"{int(line_number/lines_count*100)}%, line {line_number: }")

    file.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Creates text file with a lot of random texts, with a maximum of 1000 chars per line (+ \\n).",
    )
    parser.add_argument(
        "-f",
        "--file_name",
        type=argparse.FileType("w", encoding="UTF-8"),
        default="input_file.txt",
        help="Created file name. Default input_file.txt",
    )
    parser.add_argument(
        "-l",
        "--lines",
        type=int,
        default=1000000,
        help="Number of generated lines. Default 1000000",
    )
    args = parser.parse_args()
    write_lines(args.file_name, args.lines)
