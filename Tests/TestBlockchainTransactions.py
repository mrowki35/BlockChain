import unittest
import json

from Blockchain.Blockchain import Blockchain
from Transactions.StockTransactionFactory import StockTransactionFactory

class TestBlockchainTransactions(unittest.TestCase):

    def test_selling_shares_transaction(self):
        """
        Test dodania do blockchaina transakcji SELLING_SHARES.
        """
        blockchain = Blockchain()
        factory = StockTransactionFactory()

        tx_sell = factory.create_transaction(
            transaction_type="SELLING_SHARES",
            seller="Alice",
            buyer="Bob",
            shares=10,
            price=500.0
        )

        self.assertTrue(tx_sell.validate(), "Transakcja SELLING_SHARES powinna być ważna.")

        # Kopiemy blok z danymi transakcji
        blockchain.mineBlock(data=json.dumps(tx_sell.to_dict()))
        # W łańcuchu powinny być 2 bloki (blok genezy + 1)
        self.assertEqual(len(blockchain.chain), 2)

        # Odczytujemy dane z nowo wykopanego bloku
        new_block = blockchain.chain[1]
        block_data = json.loads(new_block.data)['data']
        block_data_type = json.loads(new_block.data)

        self.assertEqual(block_data_type["type"], "SELLING_SHARES")
        self.assertEqual(block_data["seller"], "Alice")
        self.assertEqual(block_data["buyer"], "Bob")
        self.assertEqual(block_data["shares"], 10)
        self.assertEqual(block_data["price"], 500.0)

        # Sprawdzamy poprawność łańcucha
        self.assertTrue(blockchain.validateChain())

    def test_buying_shares_transaction(self):
        """
        Test dodania do blockchaina transakcji BUYING_SHARES.
        """
        blockchain = Blockchain()
        factory = StockTransactionFactory()

        tx_buy = factory.create_transaction(
            transaction_type="BUYING_SHARES",
            seller="Charlie",
            buyer="Dave",
            shares=20,
            price=750.0
        )

        self.assertTrue(tx_buy.validate(), "Transakcja BUYING_SHARES powinna być ważna.")

        # Kopiemy blok z danymi transakcji
        blockchain.mineBlock(data=json.dumps(tx_buy.to_dict()))
        # W łańcuchu powinny być 2 bloki (blok genezy + 1)
        self.assertEqual(len(blockchain.chain), 2)

        # Odczytujemy dane z nowo wykopanego bloku
        new_block = blockchain.chain[1]
        block_data = json.loads(new_block.data)['data']
        block_data_type = json.loads(new_block.data)

        self.assertEqual(block_data_type["type"], "BUYING_SHARES")
        self.assertEqual(block_data["seller"], "Charlie")
        self.assertEqual(block_data["buyer"], "Dave")
        self.assertEqual(block_data["shares"], 20)
        self.assertEqual(block_data["price"], 750.0)

        # Sprawdzamy poprawność łańcucha
        self.assertTrue(blockchain.validateChain())

    def test_multiple_transactions(self):
        """
        Test dodania wielu bloków z różnymi transakcjami (sprzedaż i kupno).
        """
        blockchain = Blockchain()
        factory = StockTransactionFactory()

        tx1 = factory.create_transaction(
            transaction_type="SELLING_SHARES",
            seller="Alice",
            buyer="Bob",
            shares=10,
            price=500.0
        )
        tx2 = factory.create_transaction(
            transaction_type="BUYING_SHARES",
            seller="Eve",
            buyer="Frank",
            shares=15,
            price=300.0
        )
        tx3 = factory.create_transaction(
            transaction_type="SELLING_SHARES",
            seller="Grace",
            buyer="Heidi",
            shares=5,
            price=250.0
        )

        # Walidacja każdej transakcji
        self.assertTrue(tx1.validate())
        self.assertTrue(tx2.validate())
        self.assertTrue(tx3.validate())

        # Kopiemy bloki dla każdej z tych transakcji
        blockchain.mineBlock(data=json.dumps(tx1.to_dict()))
        blockchain.mineBlock(data=json.dumps(tx2.to_dict()))
        blockchain.mineBlock(data=json.dumps(tx3.to_dict()))

        # W łańcuchu: blok genezy + 3 nowe = 4
        self.assertEqual(len(blockchain.chain), 4)

        # Sprawdzamy poprawność łańcucha
        self.assertTrue(blockchain.validateChain())

if __name__ == "__main__":
    unittest.main()
