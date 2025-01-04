import unittest
import json

from Blockchain.Blockchain import Blockchain
from Transactions.VotingTransactionFactory import VotingTransactionFactory

class TestVotingTransaction(unittest.TestCase):

    def test_voting_results_transaction(self):
        """
        Test transakcji VOTING_RESULTS – tworzenie, walidacja, dodanie do blockchaina.
        """
        blockchain = Blockchain()
        voting_factory = VotingTransactionFactory()

        # Tworzymy transakcję wyników głosowania
        tx_voting = voting_factory.create_transaction(
            transaction_type="VOTING_RESULTS",
            resolution_id="Resolution-456",
            total_votes=200,
            votes_for=150,
            votes_against=30,
            votes_abstain=20
        )

        # Walidacja transakcji
        self.assertTrue(tx_voting.validate(), "Transakcja powinna być poprawna.")

        # Kopiemy blok z transakcją
        blockchain.mineBlock(data=json.dumps(tx_voting.to_dict()))
        self.assertEqual(len(blockchain.chain), 2, "W łańcuchu powinny być 2 bloki: genezy + 1 nowy.")

        # Odczyt z nowego bloku
        new_block = blockchain.chain[1]
        block_data = json.loads(new_block.data)['data']
        block_data_type = json.loads(new_block.data)

        self.assertEqual(block_data_type["type"], "VOTING_RESULTS")
        self.assertEqual(block_data["resolution_id"], "Resolution-456")
        self.assertEqual(block_data["total_votes"], 200)
        self.assertEqual(block_data["votes_for"], 150)
        self.assertEqual(block_data["votes_against"], 30)
        self.assertEqual(block_data["votes_abstain"], 20)

        # Walidacja łańcucha
        self.assertTrue(blockchain.validateChain(), "Łańcuch powinien być poprawny po dodaniu transakcji.")

    def test_voting_results_invalid_transaction(self):
        """
        Test transakcji VOTING_RESULTS – niepoprawna walidacja.
        """
        voting_factory = VotingTransactionFactory()

        # Tworzymy transakcję z niepoprawnymi danymi (sumy głosów się nie zgadzają)
        tx_invalid = voting_factory.create_transaction(
            transaction_type="VOTING_RESULTS",
            resolution_id="Resolution-789",
            total_votes=100,
            votes_for=50,
            votes_against=40,
            votes_abstain=20  # Suma to 110, nie 100
        )

        # Walidacja powinna zwrócić False
        self.assertFalse(tx_invalid.validate(), "Transakcja powinna być niepoprawna.")

if __name__ == "__main__":
    unittest.main()
