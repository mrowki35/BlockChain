from Transactions.Transaction import Transaction
from .GrantingStocksTransaction import GrantingStocksTransaction
from .IssuingStocksTransaction import IssuingStocksTransaction
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
        elif transaction_type == "ISSUING_SHARES":
            return IssuingStocksTransaction(
                company=kwargs.get("company"),
                shares=kwargs.get("shares"),
                price=kwargs.get("price")
            )
        elif transaction_type == "GRANTING_SHARES":
            return GrantingStocksTransaction(
                company=kwargs.get("company"),
                grantee=kwargs.get("grantee"),
                shares=kwargs.get("shares")
            )
        else:
            raise ValueError(f"Unsupported transaction type: {transaction_type}")
