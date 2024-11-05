import sqlite3
import logging
from abc import ABC, abstractmethod

logging.basicConfig()


class CacheProvider(ABC):
    """
    Abstract interface for provider cache
    """

    @abstractmethod
    def __enter__(self):
        """For opening files, connections etc."""
        pass

    @abstractmethod
    def __exit__(self, exception_type, exception_value, exception_traceback):
        """For closing files, connections etc."""
        pass

    @abstractmethod
    def setup(self) -> None:
        """Any setup needed before cache can be used for first time. Should not be destructive when run again."""
        pass

    @abstractmethod
    def get_line(self, file_name: str, line_number: int) -> (int, int):
        """
        Get closest previous cached line number and position in file for given file and line number.

        :param file_name: File name
        :param line_number: Required line number
        :return: Tuple with closest previous cached line number and position in file
        """
        pass

    @abstractmethod
    def store_line(self, file_name: str, line_number: int, position: int) -> None:
        """
        Store position in cache for given file name and line number.
        Every file name and line number combination should be unique.

        :param file_name: Stored file name
        :param line_number: Stored line number
        :param position: Stored position in file
        :return: None
        """
        pass

    @abstractmethod
    def _list_data(self) -> None:
        """
        Prints stored values. Has to be run with --debug
        :return: None
        """
        pass


class SQLite3Cache(CacheProvider):
    """
    Cache implementation using local SQlite3 database
    """

    def __init__(self, cache_name: str = "cache"):
        self.cache_name: str = cache_name

    def __enter__(self):
        self.connection = sqlite3.connect(f"{self.cache_name}.db")
        self.cursor = self.connection.cursor()
        return self

    def __exit__(self, exception_type, exception_value, exception_traceback):
        self.connection.close()

    def setup(self) -> None:
        if not self.cursor.execute(
            'SELECT name FROM sqlite_master WHERE type = "table" AND name = "cache"'
        ).fetchone():
            self.cursor.execute(
                """
                CREATE TABLE cache(
                    file_name TEXT NOT NULL, 
                    line_number INTEGER NOT NULL,
                    position INTEGER NOT NULL,
                    PRIMARY KEY(file_name, line_number)
                )
            """
            )
            self.connection.commit()
            logging.debug("Created table 'cache'")

    def get_line(self, file_name: str, line_number: int) -> (int, int):
        result = self.cursor.execute(
            f"""
            SELECT max(line_number), position 
            FROM cache 
            WHERE file_name = '{file_name}' AND line_number <= {line_number}
        """
        ).fetchone()
        return result[0], result[1]

    def store_line(self, file_name: str, line_number: int, position: int) -> None:
        exists = self.cursor.execute(
            f"""
            SELECT file_name, line_number, position 
            FROM cache 
            WHERE file_name = '{file_name}' AND line_number = {line_number}
        """
        ).fetchone()

        if exists:
            logging.debug(
                f"Skip storing position '{position}' for file '{file_name}', line '{line_number}'. Already contains value '{exists[2]}'"
            )
        else:
            self.cursor.execute(
                f'INSERT INTO  cache VALUES ("{file_name}", {line_number}, {position})'
            )
            self.connection.commit()
            logging.debug(
                f"Stored position '{position}' for file '{file_name}', line '{line_number}'"
            )

    def _list_data(self) -> None:
        for result in self.cursor.execute("select * from cache"):
            logging.debug(result)
