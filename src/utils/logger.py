import datetime
import logging
from enum import StrEnum
from pathlib import Path

__all__: tuple[str, ...] = ("Logger", "Colors", "LevelColors")


class Colors(StrEnum):
    """
    ANSI color codes for the logger
    """

    NAMECOLOR = "\033[38;2;147;51;234m"
    PATHCOLOR = "\033[38;2;192;38;211m"
    TIMECOLOR = "\033[38;2;52;211;153m"
    END = "\033[0m"
    BOLD = "\033[1m"
    WHITE = "\033[38;2;255;255;255m"


class LevelColors(StrEnum):
    """
    ANSI color codes for the logger levels
    """

    DEBUG = "\033[38;2;14;165;233m"
    INFO = "\033[38;2;74;222;128m"
    WARNING = "\033[38;2;250;204;21m"
    ERROR = "\033[38;2;239;68;68m"
    CRITICAL = "\033[38;2;244;63;94m"


class Formatter(logging.Formatter):
    """
    Custom formatter for the logger

    Parameters
    ----------
    name : str
        The name of the logger
    includeFileInFormatter : bool, optional
        Whether to include the file in the formatter, by default False
    """

    def __init__(self, name: str, includeFileInFormatter: bool = False) -> None:
        super().__init__()

        _name = f"{Colors.WHITE}[{Colors.END}{Colors.NAMECOLOR}{Colors.BOLD}{name}{Colors.END}{Colors.WHITE}]{Colors.END}"
        _file = f"{Colors.PATHCOLOR}%(pathname)s:%(lineno)d{Colors.END}"
        _time = f"{Colors.TIMECOLOR}%(asctime)s{Colors.END}"
        _level = f"{Colors.BOLD}{{color}}%(levelname)s{Colors.END}"

        if includeFileInFormatter:
            format = f"{_name} {_file} | {_time} | {_level} | {{color}}%(message)s {Colors.END}"
        else:
            format = f"{_name} | {_time} | {_level} | {{color}}%(message)s {Colors.END}"

        self.FORMATS = {
            level: logging.Formatter(format.format(color=color))
            for level, color in LevelColors.__members__.items()
        }

    def format(self, record: logging.LogRecord) -> str:
        """
        Format the log record

        Parameters
        ----------
        record : logging.LogRecord
            The log record to format

        Returns
        -------
        str
            The formatted log record
        """
        formatter = self.FORMATS.get(record.levelname)
        if formatter is None:
            formatter = self.FORMATS["INFO"]

        output = formatter.format(record)
        return output


class FileHandler(logging.FileHandler):
    """
    Custom file handler for the logger

    Parameters
    ----------
    ext : str
        The file extension to use
    folder : pathlib.Path | str, optional
        The folder to save the logs in, by default "logs"
    """

    _last_entry: datetime.datetime = datetime.datetime.today()

    def __init__(self, *, ext: str, folder: Path | str = "logs") -> None:
        self.folder = Path(folder)
        self.ext = ext
        self.folder.mkdir(exist_ok=True)
        super().__init__(
            self.folder / f"{datetime.datetime.today().strftime('%Y-%m-%d')}-{ext}.log",
            encoding="utf-8",
        )
        self.setFormatter(Formatter(name=ext))

    def emit(self, record: logging.LogRecord) -> None:
        """
        Emit the log record

        Parameters
        ----------
        record : logging.LogRecord
            The log record to emit

        Returns
        -------
        None
        """
        if self._last_entry.date() != datetime.datetime.today().date():
            self._last_entry = datetime.datetime.today()
            self.close()
            self.baseFilename = (
                self.folder / f"{self._last_entry.strftime('%Y-%m-%d')}-{self.ext}.log"
            ).as_posix()
            self.stream = self._open()
        super().emit(record)


class Logger(logging.Logger):
    """
    Custom logger class that extends logging.Logger to make it easier to work with

    Parameters
    ----------
    name : str
        The name of the logger
    level : int | str, optional
        The logging level, by default 0
    includeFileInFormatter : bool, optional
        Whether to include the file in the formatter, by default False
    fileLogging : bool, optional
        Whether to log to a file, by default False
    """

    def __init__(
        self,
        name: str,
        level: int | str = 0,
        includeFileInFormatter: bool = False,
        fileLogging: bool = False,
    ) -> None:
        super().__init__(name, level)

        self._handler = logging.StreamHandler()
        self._handler.setFormatter(Formatter(name, includeFileInFormatter))
        self.addHandler(self._handler)
        if fileLogging:
            self._fileHandler = FileHandler(ext=name)
            self.addHandler(self._fileHandler)
