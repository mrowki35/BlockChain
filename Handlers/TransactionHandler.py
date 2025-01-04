class TransactionHandler:
    def __init__(self):
        self.next_handler = None

    def set_next(self, handler: "TransactionHandler") -> "TransactionHandler":
        """
        Ustawia następny handler w łańcuchu.
        """
        self.next_handler = handler
        return handler

    def process(self, transaction: dict) -> bool:
        """
        Przetwarza transakcję i przekazuje ją do następnego handlera, jeśli istnieje.
        """
        if self.next_handler:
            return self.next_handler.process(transaction)
        return True
