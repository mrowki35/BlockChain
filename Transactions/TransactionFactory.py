
from Transaction import Transaction
from SellingSharesTransaction import SellingSharesTransaction
from Blockchain.Blockchain import Blockchain

import json


class TransactionFactory:
    @staticmethod
    def create_transaction(transaction_type: str, **kwargs) -> Transaction:
        if transaction_type == "SELLING_SHARES":
            return SellingSharesTransaction(
                seller=kwargs.get("seller"),
                buyer=kwargs.get("buyer"),
                shares=kwargs.get("shares"),
                price=kwargs.get("price")
            )
        else:
            raise ValueError(f"Unsupported transaction type: {transaction_type}")
        
if __name__ == "__main__":
    # Blockchain instance
    blockchain = Blockchain()

    # Create a transaction using the factory
    factory = TransactionFactory()
    transaction = factory.create_transaction(
        transaction_type="SELLING_SHARES",
        seller="Alice",
        buyer="Bob",
        shares=10,
        price=500.0
    )

    # Validate the transaction
    if transaction.validate():
        # Add the transaction to a new block in the blockchain
        blockchain.mineBlock(data=json.dumps(transaction.to_dict()))
        print("Transaction added to blockchain:")
        print(json.dumps(transaction.to_dict(), indent=4))
    else:
        print("Transaction validation failed.")