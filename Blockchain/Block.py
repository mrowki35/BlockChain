import copy


class Block:
    def __init__(self, data: list, proof: int, previous_hash: str, index: int, timestamp: str) -> None:
        """
        :param data: Lista transakcji w formie listy JSON (np. [{"type": ..., "value": ...}, ...]).
        :param proof: Wartość Proof of Work.
        :param previous_hash: Hash poprzedniego bloku.
        :param index: Indeks bloku w łańcuchu.
        :param timestamp: Znacznik czasu w formacie string.
        """
        self.data = data
        self.proof = proof
        self.previous_hash = previous_hash
        self.index = index
        self.timestamp = timestamp

    def toDictionary(self) -> dict:
        """
        Zwraca reprezentację bloku w formie słownika (JSON-ready).
        """
        return {
            "index": self.index,
            "proof": self.proof,
            "prev_hash": self.previous_hash,
            "data": self.data,
            "timestamp": self.timestamp
        }
    def clone(self):
        """
        Tworzy głęboką kopię obiektu Block.
        """
        return copy.deepcopy(self)
