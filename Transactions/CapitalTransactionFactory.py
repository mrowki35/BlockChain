from .AbstractTransactionFactory import AbstractTransactionFactory
from .Transaction import Transaction
from .IncreasingCapitalTransaction import IncreasingCapitalTransaction

class CapitalTransactionFactory(AbstractTransactionFactory):
    def create_transaction(self, **kwargs) -> Transaction:
        """
        Fabryka odpowiedzialna za transakcje związane z kapitałem.
        """
        transaction_type = kwargs.get("transaction_type", "")

        if transaction_type == "INCREASING_CAPITAL":
            return IncreasingCapitalTransaction(
                company=kwargs.get("company"),
                additional_capital=kwargs.get("additional_capital"),
                new_shares=kwargs.get("new_shares")
            )
        else:
            raise ValueError(f"Unsupported transaction type for CapitalTransactionFactory: {transaction_type}")
