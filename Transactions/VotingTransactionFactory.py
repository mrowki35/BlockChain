from .AbstractTransactionFactory import AbstractTransactionFactory
from .Transaction import Transaction
from .VotingResultsTransaction import VotingResultsTransaction


class VotingTransactionFactory(AbstractTransactionFactory):
    """
    Fabryka odpowiedzialna za transakcje związane z wynikami głosowania.
    """

    def create_transaction(self, **kwargs) -> Transaction:
        transaction_type = kwargs.get("transaction_type", "")

        if transaction_type == "VOTING_RESULTS":
            return VotingResultsTransaction(
                resolution_id=kwargs.get("resolution_id"),
                total_votes=kwargs.get("total_votes"),
                votes_for=kwargs.get("votes_for"),
                votes_against=kwargs.get("votes_against"),
                votes_abstain=kwargs.get("votes_abstain")
            )
        else:
            raise ValueError(f"Unsupported transaction type for VotingTransactionFactory: {transaction_type}")
