import argparse
from cache import CacheProvider, SQLite3Cache
import logging

logging.basicConfig()


class LineReader:
    """
    Reader for large files which uses cache to speed up additional executions.
    """

    def __init__(self, file_name: str, indexing_interval: int, cache: CacheProvider):
        """
        :param file_name: Name of the file to read
        :param indexing_interval: How often the line position in file should be stored during file traversal
        :param cache: Cache provider used for caching
        """
        self.file_name: str = file_name
        self.indexing_interval: int = indexing_interval
        self.cache: CacheProvider = cache

    def get_line(self, line_number: int) -> str | None:
        """
        Gets text on line given by line number

        :param line_number: Line number to get
        :return: Text on given line or None if file is shorter
        """
        current_line_number, current_position = self.cache.get_line(
            self.file_name, line_number
        )

        with open(self.file_name, "r", encoding="UTF-8", newline="") as file:
            # Seek to line itself or nearest previous line if stored in cache
            if current_line_number is None:
                current_line_number, current_position = 0, 0
            else:
                file.seek(current_position)
                logging.debug(f"Got position {current_position} for line {line_number}")

            # Read file until required line is found
            while True:
                line = file.readline()

                if not line:
                    raise EOFError(f"File has only {current_line_number} lines")

                if current_line_number == line_number:
                    self.cache.store_line(
                        self.file_name, current_line_number, current_position
                    )
                    return line[: -len(file.newlines)]

                if (
                    current_line_number > 0
                    and self.indexing_interval > 0
                    and current_line_number % self.indexing_interval == 0
                ):
                    self.cache.store_line(
                        self.file_name, current_line_number, current_position
                    )

                current_line_number += 1
                current_position += len(line)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Prints an arbitrary line from the file.\n"
        "Caches line positions for faster retrival on additional runs.\n"
        "Cache is stored in file cache.db in te root of the project.",
    )
    parser.add_argument("input_file", nargs="?", default="input_file.txt")
    parser.add_argument("index", nargs="?", default=0, type=int)
    parser.add_argument(
        "-i",
        "--indexing_interval",
        type=int,
        default=1000,
        help="Set how often new lines are cached during file traversal. Set to 0 to disable continuous indexing. Default 1000",
    )
    parser.add_argument(
        "--debug",
        action=argparse.BooleanOptionalAction,
        help="See debug messages",
    )
    args = parser.parse_args()

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)

    with SQLite3Cache() as cache_provider:
        cache_provider.setup()
        reader = LineReader(args.input_file, args.indexing_interval, cache_provider)
        line = reader.get_line(args.index)
        if line:
            print(line)
