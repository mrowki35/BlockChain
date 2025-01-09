import unittest
from Handlers.ValidationHandler import ValidationHandler
from Handlers.ComplianceHandler import ComplianceHandler
from Handlers.ExecutionHandler import ExecutionHandler


class TestTransactionHandlers(unittest.TestCase):
    def setUp(self):
        # Tworzenie łańcucha odpowiedzialności
        self.validation_handler = ValidationHandler()
        self.compliance_handler = ComplianceHandler()
        self.execution_handler = ExecutionHandler()

        self.validation_handler.set_next(self.compliance_handler).set_next(self.execution_handler)

    def test_valid_transaction(self):
        transaction = {
            "transaction_type": "TRANSFER",
            "amount": 50.0,
            "sender": "Alice",
            "receiver": "Bob"
        }

        result = self.validation_handler.process(transaction)
        self.assertTrue(result)

    def test_missing_field(self):
        transaction = {
            "transaction_type": "TRANSFER",
            "amount": 50.0,
            "sender": "Alice"
        }

        result = self.validation_handler.process(transaction)
        self.assertFalse(result)

    def test_compliance_failure(self):
        transaction = {
            "transaction_type": "TRANSFER",
            "amount": 50.0,
            "sender": "Alice",
            "receiver": "Alice"
        }

        result = self.validation_handler.process(transaction)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main()
