import unittest
import json

from Blockchain.Blockchain import Blockchain
from Transactions.TransactionFactory import TransactionFactory

class TestBlockchainSellingShares(unittest.TestCase):
    def test_three_selling_shares_transactions(self):
        # 1. Tworzymy blockchain
        blockchain = Blockchain()

        # 2. Tworzymy fabrykę transakcji
        factory = TransactionFactory()

        # 3. Generujemy trzy transakcje typu SELLING_SHARES
        tx1 = factory.create_transaction(
            transaction_type="SELLING_SHARES",
            seller="Alice",
            buyer="Bob",
            shares=10,
            price=500.0
        )
        tx2 = factory.create_transaction(
            transaction_type="SELLING_SHARES",
            seller="John",
            buyer="Kate",
            shares=5,
            price=300.0
        )
        tx3 = factory.create_transaction(
            transaction_type="SELLING_SHARES",
            seller="Mike",
            buyer="Sara",
            shares=12,
            price=750.0
        )

        # 4. Walidujemy każdą transakcję przed dodaniem do blockchaina
        self.assertTrue(tx1.validate(), "Pierwsza transakcja SELLING_SHARES powinna być prawidłowa.")
        self.assertTrue(tx2.validate(), "Druga transakcja SELLING_SHARES powinna być prawidłowa.")
        self.assertTrue(tx3.validate(), "Trzecia transakcja SELLING_SHARES powinna być prawidłowa.")

        # 5. Kopiemy blok dla każdej transakcji (dodajemy do łańcucha)
        blockchain.mineBlock(data=json.dumps(tx1.to_dict()))
        blockchain.mineBlock(data=json.dumps(tx2.to_dict()))
        blockchain.mineBlock(data=json.dumps(tx3.to_dict()))

        # Powinno być 1 (blok genezy) + 3 nowe bloki = 4
        self.assertEqual(
            len(blockchain.chain),
            4,
            "W łańcuchu powinny być 4 bloki (1 genezy i 3 nowe transakcje)."
        )

        # 6. Sprawdzamy dane w kopanych blokach
        # Indeksy: 0 -> blok genezy, 1 -> tx1, 2 -> tx2, 3 -> tx3
        block_tx1 = blockchain.chain[1]
        block_tx2 = blockchain.chain[2]
        block_tx3 = blockchain.chain[3]

        # Odczytujemy dane z bloków
        data_tx1 = json.loads(block_tx1.data)
        data_tx2 = json.loads(block_tx2.data)
        data_tx3 = json.loads(block_tx3.data)

        # Weryfikujemy, czy dane w blokach są takie, jak w oryginalnych transakcjach
        self.assertEqual(data_tx1["transaction_type"], "SELLING_SHARES")
        self.assertEqual(data_tx1["seller"], "Alice")
        self.assertEqual(data_tx1["buyer"], "Bob")
        self.assertEqual(data_tx1["shares"], 10)
        self.assertEqual(data_tx1["price"], 500.0)

        self.assertEqual(data_tx2["transaction_type"], "SELLING_SHARES")
        self.assertEqual(data_tx2["seller"], "John")
        self.assertEqual(data_tx2["buyer"], "Kate")
        self.assertEqual(data_tx2["shares"], 5)
        self.assertEqual(data_tx2["price"], 300.0)

        self.assertEqual(data_tx3["transaction_type"], "SELLING_SHARES")
        self.assertEqual(data_tx3["seller"], "Mike")
        self.assertEqual(data_tx3["buyer"], "Sara")
        self.assertEqual(data_tx3["shares"], 12)
        self.assertEqual(data_tx3["price"], 750.0)

        # 7. Na koniec sprawdzamy, czy cały łańcuch jest poprawny
        self.assertTrue(
            blockchain.validateChain(),
            "Łańcuch powinien być poprawny po dodaniu 3 transakcji SELLING_SHARES."
        )

if __name__ == "__main__":
    unittest.main()
