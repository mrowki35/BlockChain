from .Block import Block
import datetime as dt
import hashlib
import json
class Blockchain:
    def __init__(self) -> None:
        self.chain = []
        # Dla przykładu tworzymy blok genezy
        genesis_block = self.createBlock(
            data="Genesis Block",
            proof=1,
            prev_hash="0",
            index=0
        )
        self.chain.append(genesis_block)

    def createBlock(self, data, proof, prev_hash, index) -> Block:
        block = Block(
            data=data,
            proof=proof,
            previous_hash=prev_hash,
            index=index,
            timestamp=str(dt.datetime.now())
        )
        return block

    def getPreviuosBlock(self) -> Block:
        return self.chain[-1]

    def mineBlock(self, data: str) -> Block:
        prevBlock = self.getPreviuosBlock()
        prevProof = prevBlock.proof
        index = prevBlock.index + 1
        proof = self.proofOfWork(prevProof, index, data)
        previousHash = self.hashBlock(prevBlock)
        block = self.createBlock(
            data=data,
            proof=proof,
            prev_hash=previousHash,
            index=index
        )
        self.chain.append(block)
        return block

    def proofOfWork(self, prev_proof, index, data) -> int:
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

    def hashBlock(self, block: Block) -> str:
        encoded_block = json.dumps(block.toDictionary(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def digest(self, new_proof, previous_proof, index, data) -> bytes:
        """
        Przykładowa funkcja haszująca: (new_proof^2 - previous_proof^2 + index) + data
        """
        to_digest = str(new_proof**2 - previous_proof**2 + index) + data
        return to_digest.encode()

    def validateChain(self) -> bool:
        """
        Metoda weryfikująca poprawność całego łańcucha.
        """
        currentBlock = self.chain[0]
        block_index = 1

        while block_index < len(self.chain):
            nextBlock = self.chain[block_index]
            # Sprawdzamy, czy hash poprzedniego bloku jest zgodny
            if nextBlock.previous_hash != self.hashBlock(currentBlock):
                return False

            # Sprawdzamy dowód pracy
            currentProof = currentBlock.proof
            next_index, next_data, next_proof = (
                nextBlock.index,
                nextBlock.data,
                nextBlock.proof
            )
            hashValue = hashlib.sha256(
                self.digest(
                    new_proof=next_proof,
                    previous_proof=currentProof,
                    index=next_index,
                    data=next_data
                )
            ).hexdigest()

            # W tym przykładzie sprawdzamy, czy pierwsze cztery znaki to '0000'
            # (w powyższej implementacji w `mineBlock` było "000000", więc można
            #  tu dostosować warunek w zależności od wymagań)
            if hashValue[:2] != "00":
                return False

            currentBlock = nextBlock
            block_index += 1

        return True

    # ------------------------------
    # Implementacja iteratora
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