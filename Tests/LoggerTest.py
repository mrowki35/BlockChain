import os
import pytest
from Logging.Logger import Logger

TEST_LOG_FILE = "test_log.log"

@pytest.fixture(scope="function", autouse=True)
def cleanup_test_log_file():
    """
    Fixture to ensure the test log file is cleaned up before each test.
    """
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)
    yield
    if os.path.exists(TEST_LOG_FILE):
        os.remove(TEST_LOG_FILE)

def test_singleton_behavior():
    """Test that Logger is a singleton."""
    logger1 = Logger(file_name=TEST_LOG_FILE)
    logger2 = Logger(file_name="ignored_file.log")
    logger3 = Logger()

    assert logger1 is logger2, "Logger instances are not the same (singleton failed)"
    assert logger1 is logger3, "Logger instances are not the same (singleton failed)"

def test_logging_to_same_file():
    """Test that all Logger instances log to the same file."""
    logger1 = Logger(file_name=TEST_LOG_FILE)
    logger2 = Logger()
    logger3 = Logger()

    logger1.log("Application started.")
    logger2.warning("This is a warning from logger2.")
    logger3.error("Critical issue logged by logger3!", "CRITICAL")


    assert os.path.exists(TEST_LOG_FILE), "Log file was not created"

    with open(TEST_LOG_FILE, "r") as log_file:
        logs = log_file.readlines()

    assert len(logs) == 3, f"Expected 3 log entries, found {len(logs)}"
    assert "Application started." in logs[0], "First log entry missing or incorrect"
    assert "This is a warning from logger2." in logs[1], "Second log entry missing or incorrect"
    assert "Critical issue logged by logger3!" in logs[2], "Third log entry missing or incorrect"

def test_logging_severity_enum():
    """Test logging with Severity enum."""
    from Blockchain.Logging.Logger import Severity

    logger = Logger(file_name=TEST_LOG_FILE)

    logger.error("Low severity error", Severity.LOW)
    logger.error("Blocker severity error", Severity.BLOCKER)

    with open(TEST_LOG_FILE, "r") as log_file:
        logs = log_file.readlines()

   
    assert len(logs) == 2, f"Expected 2 log entries, found {len(logs)}"
    assert "[ERROR-LOW] Low severity error" in logs[0], "Severity LOW log entry incorrect"
    assert "[ERROR-BLOCKER] Blocker severity error" in logs[1], "Severity BLOCKER log entry incorrect"
