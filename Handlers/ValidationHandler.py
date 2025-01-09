from .TransactionHandler import TransactionHandler


class ValidationHandler(TransactionHandler):
    def process(self, transaction: dict) -> bool:
        """
        Waliduje transakcję.
        """
        required_fields = ["transaction_type", "amount", "sender", "receiver"]
        for field in required_fields:
            if field not in transaction:
                print(f"Validation failed: Missing field '{field}'")
                return False

        if transaction["amount"] <= 0:
            print("Validation failed: Amount must be greater than zero.")
            return False

        print("Validation passed.")
        return super().process(transaction)
