from .BlockBuilder import BlockBuilder
from .Block import Block
import hashlib
import json
from Logging.Logger import Logger

logger = Logger()


class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        # Tworzymy blok genezy za pomocą BlockBuilder
        genesis_block = BlockBuilder() \
            .set_data("Genesis Block") \
            .set_proof(1) \
            .set_previous_hash("0") \
            .set_index(0) \
            .set_timestamp() \
            .build()
        self.chain.append(genesis_block)

    def get_previous_block(self) -> Block:
        """
        Zwraca ostatni blok w łańcuchu.
        """
        return self.chain[-1]

    def mine_block(self, data: str) -> Block:
        """
        Kopie nowy blok, dodając go do łańcucha.
        :param data: Dane do zapisania w nowym bloku.
        """
        prev_block = self.get_previous_block()
        prev_proof = prev_block.proof
        index = prev_block.index + 1
        proof = self.proof_of_work(prev_proof, index, data)
        previous_hash = self.hash_block(prev_block)

        # Budujemy nowy blok za pomocą BlockBuilder
        new_block = BlockBuilder() \
            .set_data(data) \
            .set_proof(proof) \
            .set_previous_hash(previous_hash) \
            .set_index(index) \
            .set_timestamp() \
            .build()

        self.chain.append(new_block)
        return new_block

    def proof_of_work(self, prev_proof, index, data) -> int:
        """
        Oblicza Proof of Work dla nowego bloku.
        """
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_dig = self.digest(new_proof, prev_proof, index, data)
            hash_value = hashlib.sha256(to_dig).hexdigest()
            if hash_value[:2] == "00":
                check_proof = True
            else:
                new_proof += 1
        return new_proof

    def hash_block(self, block: Block) -> str:
        """
        Liczy hash bloku.
        """
        encoded_block = json.dumps(block.toDictionary(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def digest(self, new_proof, previous_proof, index, data) -> bytes:
        """
        Funkcja pomocnicza do generowania wartości haszowania.
        """
        to_digest = str(new_proof ** 2 - previous_proof ** 2 + index) + json.dumps(data, sort_keys=True)
        return to_digest.encode()

    def validate_chain(self) -> bool:
        """
        Weryfikuje poprawność całego łańcucha.
        """
        current_block = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            next_block = self.chain[block_index]
            if next_block.previous_hash != self.hash_block(current_block):
                return False

            current_proof = current_block.proof
            next_index, next_data, next_proof = (
                next_block.index,
                next_block.data,
                next_block.proof
            )
            hash_value = hashlib.sha256(
                self.digest(
                    new_proof=next_proof,
                    previous_proof=current_proof,
                    index=next_index,
                    data=next_data
                )
            ).hexdigest()

            if hash_value[:2] != "00":
                return False

            current_block = next_block
            block_index += 1

        return True

    # ------------------------------
    # Iterator dla Blockchain
    # ------------------------------
    def __iter__(self):
        self._current_index = 0
        return self

    def __next__(self):
        if self._current_index < len(self.chain):
            block = self.chain[self._current_index]
            self._current_index += 1
            return block
        else:
            raise StopIteration
