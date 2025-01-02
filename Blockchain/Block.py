class Block:
    def __init__(self, data: str, proof: int, previous_hash: str, index: int, timestamp: str) -> None:
        self.data = data
        self.proof = proof
        self.previous_hash = previous_hash
        self.index = index
        self.timestamp = timestamp

    def toDictionary(self) -> dict:
        return {
            "index": self.index,
            "proof": self.proof,
            "prev_hash": self.previous_hash,
            "data": self.data,
            "timestamp": self.timestamp
        }