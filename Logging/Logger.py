import threading
from datetime import datetime
from SeverityEnum import Severity

from enum import Enum, auto
# class Severity(Enum):
#     """Enumeration for log severity levels."""
#     LOW = auto()
#     MEDIUM = auto()
#     HIGH = auto()
#     CRITICAL = auto()
#     BLOCKER = auto()

class Logger:
    _instance = None
    _lock = threading.Lock()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            with cls._lock:
                if not cls._instance:
                    cls._instance = super().__new__(cls)
                    cls._instance.initialize(*args, **kwargs)
        return cls._instance

    def initialize(self, file_name="application.log"):
        if hasattr(self, "_initialized") and self._initialized:
            return
        self.file_name = file_name
        self._initialized = True

    def _get_timestamp(self) -> str:
        """Returns the current date and time as a formatted string."""
        return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def log(self, message: str):
        """Logs a general message."""
        self._write_log("INFO", message)

    def warning(self, message: str):
        """Logs a warning message."""
        self._write_log("WARNING", message)

    def error(self, message: str):
        """Logs an error message."""
        self._write_log("ERROR", message)

    def error(self, message: str, severity: Severity):
        """Logs an error message with a specified severity from the Severity enum."""
        if not isinstance(severity, Severity):
            raise ValueError("Severity must be an instance of the Severity enum.")
        self._write_log(f"ERROR-{severity.name}", message)


    def _write_log(self, level: str, message: str):
        """Writes a log entry with the specified level and message."""
        timestamp = self._get_timestamp()
        log_entry = f"{timestamp} [{level}] {message}"
        with open(self.file_name, "a") as log_file:
            log_file.write(log_entry + "\n")
        #print(log_entry) 


