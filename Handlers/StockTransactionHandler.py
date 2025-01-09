from Handlers.TransactionHandler import TransactionHandler
from Transactions.PayingDividendsTransaction import PayingDividendsTransaction
from Transactions.Transaction import Transaction


class DividendTransactionHandler(TransactionHandler):
    def process(self, transaction: Transaction) -> bool:
        """
        Walidacja transakcji dywidendowych.
        """
        if isinstance(transaction, PayingDividendsTransaction):
            if transaction.data['dividend_per_share'] <= 0 or transaction.data['shares'] <= 0:
                print("Validation failed: Invalid dividend parameters.")
                return False

        print("Dividend transaction validation passed.")
        return super().process(transaction)
