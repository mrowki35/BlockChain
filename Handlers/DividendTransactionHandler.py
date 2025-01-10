from .base_handler import TransactionHandler
from Transactions.DividendFactory import DividendFactory


class DividendTransactionHandler(TransactionHandler):
    """
    Handler dla transakcji wypłaty dywidend (PAYING_DIVIDENDS).
    """

    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        self.factory = DividendFactory()

    def handle(self, transaction_data: dict):
        t_type = transaction_data.get("transaction_type", "")
        if t_type == "PAYING_DIVIDENDS":
            transaction = self.factory.create_transaction(**transaction_data)
            if transaction.validate():
                print(f"[DividendTransactionHandler] Transaction validated: {transaction.to_dict()}")
            else:
                print(f"[DividendTransactionHandler] Transaction invalid: {transaction.to_dict()}")
            return transaction
        else:
            if self._next_handler:
                return self._next_handler.save(transaction_data)
            else:
                return None
