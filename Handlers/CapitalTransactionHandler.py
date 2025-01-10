from .base_handler import TransactionHandler
from Transactions.CapitalTransactionFactory import CapitalTransactionFactory
from .save_handler import SaveHandler


class CapitalTransactionHandler(TransactionHandler):
    """
    Handler dla transakcji typu: INCREASING_CAPITAL itp.
    """

    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        self.factory = CapitalTransactionFactory()

    def handle(self, transaction_data: dict):
        t_type = transaction_data.get("transaction_type", "")
        if t_type == "INCREASING_CAPITAL":
            transaction = self.factory.create_transaction(**transaction_data)
            if transaction.validate():
                print(f"[CapitalTransactionHandler] Transaction validated: {transaction.to_dict()}")
                return transaction
            else:
                print(f"[CapitalTransactionHandler] Transaction invalid: {transaction.to_dict()}")
                return None
        else:
            if self._next_handler:
                return self._next_handler.save(transaction_data)
            else:
                return None
