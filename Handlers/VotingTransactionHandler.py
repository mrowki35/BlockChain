from .base_handler import TransactionHandler
from Transactions.VotingTransactionFactory import VotingTransactionFactory
from Logging.Logger import Logger
logger=Logger()

class VotingTransactionHandler(TransactionHandler):
    """
    Handler dla transakcji dotyczących głosowania (VOTING_RESULTS).
    """

    def __init__(self, next_handler=None):
        super().__init__(next_handler)
        self.factory = VotingTransactionFactory()

    def handle(self, transaction_data: dict):
        t_type = transaction_data.get("transaction_type", "")
        if t_type == "VOTING_RESULTS":
            transaction = self.factory.create_transaction(**transaction_data)
            if transaction.validate():
                logger.log(f"[VotingTransactionHandler] Transaction validated: {transaction.to_dict()}")
                return transaction
            else:
                logger.log(f"[VotingTransactionHandler] Transaction invalid: {transaction.to_dict()}")
                return None

        else:
            if self._next_handler:
                return self._next_handler.save(transaction_data)
            else:
                return None
