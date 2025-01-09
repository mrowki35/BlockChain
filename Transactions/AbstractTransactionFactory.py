from abc import ABC, abstractmethod
from .Transaction import Transaction


class AbstractTransactionFactory(ABC):

    @abstractmethod
    def create_transaction(self, **kwargs) -> Transaction:
        """
        Tworzy obiekt transakcji.
        """
        pass
