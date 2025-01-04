from .TransactionHandler import TransactionHandler


class ComplianceHandler(TransactionHandler):
    def process(self, transaction: dict) -> bool:
        """
        Sprawdza zgodność transakcji z zasadami.
        """
        if transaction["sender"] == transaction["receiver"]:
            print("Compliance failed: Sender and receiver cannot be the same.")
            return False

        print("Compliance passed.")
        return super().process(transaction)
