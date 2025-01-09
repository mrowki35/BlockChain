import unittest
from Blockchain.Blockchain import Blockchain


class TestBlockchainIterator(unittest.TestCase):
    def test_blockchain_iteration(self):
        blockchain = Blockchain()

        # Dodajmy kilka bloków
        blockchain.mine_block("Test1")
        blockchain.mine_block("Test2")
        blockchain.mine_block("Test3")

        # Przekształcamy obiekt blockchain w listę za pomocą list(...)
        blocks_list = list(blockchain)

        # Sprawdzamy, czy w liście są 4 bloki (1 blok genezy + 3 nowe)
        self.assertEqual(len(blocks_list), 4)

        # Sprawdzamy, czy dane w blokach się zgadzają
        self.assertEqual(blocks_list[1].data, "Test1")
        self.assertEqual(blocks_list[2].data, "Test2")
        self.assertEqual(blocks_list[3].data, "Test3")

    def test_validate_chain_correct(self):
        """
        Sprawdza, czy łańcuch jest poprawny po wykopaniu kilku bloków
        (bez manipulacji danymi).
        """
        blockchain = Blockchain()

        # Kopiemy kilka bloków
        blockchain.mine_block("Block #1 data")
        blockchain.mine_block("Block #2 data")
        blockchain.mine_block("Block #3 data")

        # Powinno zwrócić True, bo nikt nie manipulował blokami.
        self.assertTrue(blockchain.validate_chain())

    def test_validate_chain_broken(self):
        """
        Sprawdza, czy łańcuch zostanie uznany za niepoprawny,
        gdy zmodyfikujemy dane w jednym z bloków.
        """
        blockchain = Blockchain()

        # Kopiemy kilka bloków
        blockchain.mine_block("Block #1 data")
        blockchain.mine_block("Block #2 data")
        blockchain.mine_block("Block #3 data")

        # Symulujemy manipulację danymi w drugim bloku (o indeksie [1])
        blockchain.chain[1].data = "Manipulated data"

        # Powinno zwrócić False, bo łańcuch został uszkodzony
        self.assertFalse(blockchain.validate_chain())


if __name__ == "__main__":
    unittest.main()
