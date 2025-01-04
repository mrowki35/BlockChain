from Transactions.Transaction import Transaction
from .SellingSharesTransaction import SellingSharesTransaction
from .BuyingSharesTransaction import BuyingSharesTransaction
from .AbstractTransactionFactory import AbstractTransactionFactory


class StockTransactionFactory(AbstractTransactionFactory):
    def create_transaction(self, **kwargs) -> Transaction:
        transaction_type = kwargs.get("transaction_type", "")
        if transaction_type == "SELLING_SHARES":
            return SellingSharesTransaction(
                seller=kwargs.get("seller"),
                buyer=kwargs.get("buyer"),
                shares=kwargs.get("shares"),
                price=kwargs.get("price")
            )
        elif transaction_type == "BUYING_SHARES":
            return BuyingSharesTransaction(
                seller=kwargs.get("seller"),
                buyer=kwargs.get("buyer"),
                shares=kwargs.get("shares"),
                price=kwargs.get("price")
            )
        else:
            raise ValueError(f"Unsupported transaction type: {transaction_type}")
