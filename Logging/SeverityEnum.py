from enum import Enum, auto
class Severity(Enum):
    """Enumeration for log severity levels."""
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()
    CRITICAL = auto()
    BLOCKER = auto()