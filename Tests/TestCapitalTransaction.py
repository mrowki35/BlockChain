import unittest
import json

from Blockchain.Blockchain import Blockchain
from Transactions.CapitalTransactionFactory import CapitalTransactionFactory


class TestCapitalTransaction(unittest.TestCase):

    def test_increasing_capital_transaction(self):
        """
        Test transakcji INCREASING_CAPITAL
        tworzonej przez CapitalTransactionFactory.
        """
        blockchain = Blockchain()
        capital_factory = CapitalTransactionFactory()

        # Tworzymy transakcję zwiększania kapitału
        tx_increase = capital_factory.create_transaction(
            transaction_type="INCREASING_CAPITAL",
            company="Beta Sp. z o.o.",
            additional_capital=10000.0,
            new_shares=20
        )

        self.assertTrue(tx_increase.validate(), "Transakcja powinna być poprawna.")

        # Dodajemy do blockchaina
        blockchain.mineBlock(data=json.dumps(tx_increase.to_dict()))
        self.assertEqual(len(blockchain.chain), 2, "W łańcuchu powinny być 2 bloki: genezy + 1 nowy.")

        # Odczyt z nowego bloku
        new_block = blockchain.chain[1]
        block_data = json.loads(new_block.data)['data']
        block_data_type = json.loads(new_block.data)

        self.assertEqual(block_data_type["type"], "INCREASING_CAPITAL")
        self.assertEqual(block_data["company"], "Beta Sp. z o.o.")
        self.assertEqual(block_data["additional_capital"], 10000.0)
        self.assertEqual(block_data["new_shares"], 20)

        # Walidacja łańcucha
        self.assertTrue(blockchain.validateChain(), "Łańcuch powinien być poprawny po dodaniu transakcji.")


if __name__ == "__main__":
    unittest.main()
