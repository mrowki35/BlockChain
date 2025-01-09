from Handlers.TransactionHandler import TransactionHandler
from Transactions.Transaction import Transaction


class GeneralValidationHandler(TransactionHandler):
    def process(self, transaction: Transaction) -> bool:
        """
        Ogólna walidacja transakcji, np. sprawdzenie pól wspólnych dla wszystkich typów.
        """
        if not transaction.data['company']:
            print("Validation failed: Missing 'company' field.")
            return False
        if hasattr(transaction, "amount") and transaction.data['amount'] <= 0:
            print("Validation failed: 'amount' must be greater than zero.")
            return False

        print("General validation passed.")
        return super().process(transaction)
