from .TransactionHandler import TransactionHandler


class ExecutionHandler(TransactionHandler):
    def process(self, transaction: dict) -> bool:
        """
        Wykonuje transakcję.
        """
        print(f"Executing transaction: {transaction}")
        # Symulacja zapisu transakcji do systemu lub blockchaina
        return super().process(transaction)
