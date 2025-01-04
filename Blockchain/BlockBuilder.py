from .Block import Block
import datetime as dt


class BlockBuilder:
    def __init__(self):
        """
        Inicjalizuje pusty obiekt BlockBuilder.
        """
        self.data = None
        self.proof = None
        self.previous_hash = None
        self.index = None
        self.timestamp = None

    def set_data(self, data: str) -> "BlockBuilder":
        """
        Ustawia dane bloku.
        :param data: Treść (np. transakcje) do zapisania w bloku.
        """
        self.data = data
        return self

    def set_proof(self, proof: int) -> "BlockBuilder":
        """
        Ustawia wartość Proof of Work.
        :param proof: Wartość dowodu pracy.
        """
        self.proof = proof
        return self

    def set_previous_hash(self, previous_hash: str) -> "BlockBuilder":
        """
        Ustawia hash poprzedniego bloku.
        :param previous_hash: Hash poprzedniego bloku.
        """
        self.previous_hash = previous_hash
        return self

    def set_index(self, index: int) -> "BlockBuilder":
        """
        Ustawia indeks bloku.
        :param index: Indeks bloku w łańcuchu.
        """
        self.index = index
        return self

    def set_timestamp(self, timestamp: str = None) -> "BlockBuilder":
        """
        Ustawia znacznik czasu (domyślnie bieżący czas).
        :param timestamp: Znacznik czasu w formacie string (opcjonalnie).
        """
        self.timestamp = timestamp or str(dt.datetime.now())
        return self

    def build(self) -> Block:
        """
        Buduje i zwraca kompletny obiekt Block.
        """
        if None in (self.data, self.proof, self.previous_hash, self.index, self.timestamp):
            raise ValueError("Nie ustawiono wszystkich wymaganych właściwości bloku.")

        return Block(
            data=self.data,
            proof=self.proof,
            previous_hash=self.previous_hash,
            index=self.index,
            timestamp=self.timestamp
        )
