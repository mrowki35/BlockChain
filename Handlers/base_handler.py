from abc import ABC, abstractmethod


class TransactionHandler(ABC):
    """
    Klasa bazowa (abstrakcyjna) dla handlera w chain of responsibility.
    """

    def __init__(self, next_handler=None):
        self._next_handler = next_handler

    @abstractmethod
    def handle(self, transaction_data: dict):
        """
        Próbuje utworzyć (i ew. zwalidować) transakcję na podstawie transaction_data.
        Jeśli nie rozpoznaje typu transakcji, deleguje do next_handler.
        """
        pass

    def set_next(self, handler: "TransactionHandler"):
        """
        Ustawia kolejny handler w łańcuchu.
        """
        self._next_handler = handler
        return handler  # można zwrócić dla ładnego chainingu
