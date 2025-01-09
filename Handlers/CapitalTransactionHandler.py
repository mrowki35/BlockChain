from Handlers.TransactionHandler import TransactionHandler
from Transactions.IncreasingCapitalTransaction import IncreasingCapitalTransaction
from Transactions.Transaction import Transaction


class CapitalTransactionHandler(TransactionHandler):
    def process(self, transaction: Transaction) -> bool:
        """
        Walidacja transakcji kapitałowych.
        """
        if isinstance(transaction, IncreasingCapitalTransaction):
            if transaction.data['additional_capital'] <= 0 or transaction.data['new_shares'] <= 0:
                print("Validation failed: Invalid capital increase parameters.")
                return False

        print("Capital transaction validation passed.")
        return super().process(transaction)
