class Block:
    def __init__(self,data:str,proof:int, previus_hash: str,index:int, timestamp: str) -> None:
        self.index = index
        self.proof= proof
        self.previous_hash=previus_hash
        self.index=index
        self.timestamp=timestamp

    def toDictionary(self)->dict:
        return {"index": self.index,
                "proof": self.proof,
                "prev_hash": self.previous_hash,
                "index": self.index,
                "timestamp": self.timestamp
                }