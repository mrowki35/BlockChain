from .base_handler import TransactionHandler
from Transactions.StockTransactionFactory import StockTransactionFactory
from Transactions.Transaction import Transaction


class StockTransactionHandler(TransactionHandler):
    """
    Handler odpowiedzialny za transakcje na akcjach (akcje, sprzedaż, kupno itp.).
    """

    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        self.factory = StockTransactionFactory()  # wewnętrzna fabryka

    def handle(self, transaction_data: dict):
        # Sprawdzamy, czy klucz "transaction_type" jest w obsługiwanych
        t_type = transaction_data.get("transaction_type", "")
        supported_types = ["SELLING_SHARES", "BUYING_SHARES", "ISSUING_SHARES", "GRANTING_SHARES"]

        if t_type in supported_types:
            # Stworzymy transakcję przez fabrykę
            transaction = self.factory.create_transaction(**transaction_data)
            # Walidacja transakcji
            if transaction.validate():
                print(f"[StockTransactionHandler] Transaction validated: {transaction.to_dict()}")
            else:
                print(f"[StockTransactionHandler] Transaction invalid: {transaction.to_dict()}")

            # Możemy zwrócić transakcję lub None
            return transaction
        else:
            # Delegujemy do next_handler
            if self._next_handler:
                return self._next_handler.save(transaction_data)
            else:
                return None
