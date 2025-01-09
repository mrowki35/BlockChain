from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any
import requests
from ..Blockchain.Blockchain import Blockchain
from ..Blockchain.Block import Block

app = FastAPI()

# Tworzymy instancję blockchain
blockchain = Blockchain()

# Model Pydantic dla dodania danych
class DataModel(BaseModel):
    data: str

# Model Pydantic dla synchronizacji bloków
class BlockModel(BaseModel):
    index: int
    proof: int
    previous_hash: str
    data: Any
    timestamp: str

@app.get("/chain", response_model=List[Dict[str, Any]])
def get_chain():
    """
    Zwraca cały łańcuch bloków.
    """
    return [block.toDictionary() for block in blockchain.chain]

@app.post("/mine")
def mine_block(data: DataModel):
    """
    Tworzy nowy blok z podanymi danymi.
    """
    new_block = blockchain.mine_block(data.data)
    return {"message": "Block mined successfully!", "block": new_block.toDictionary()}

@app.get("/validate")
def validate_chain():
    """
    Sprawdza, czy łańcuch jest poprawny.
    """
    is_valid = blockchain.validate_chain()
    if is_valid:
        return {"message": "Blockchain is valid!"}
    else:
        raise HTTPException(status_code=400, detail="Blockchain is invalid!")

@app.post("/add_block")
def add_block(block: BlockModel):
    """
    Dodaje blok do łańcucha (synchronizacja między węzłami).
    """
    new_block = Block(
        data=block.data,
        proof=block.proof,
        previous_hash=block.previous_hash,
        index=block.index,
        timestamp=block.timestamp
    )
    previous_block = blockchain.get_previous_block()
    if new_block.previous_hash != blockchain.hash_block(previous_block):
        raise HTTPException(status_code=400, detail="Previous hash does not match!")
    if not blockchain.proof_of_work(previous_block.proof, new_block.index, new_block.data) == new_block.proof:
        raise HTTPException(status_code=400, detail="Proof of work is invalid!")
    blockchain.chain.append(new_block)
    return {"message": "Block added successfully!"}

@app.post("/sync")
def sync_chain(neighbor: str):
    """
    Synchronizuje łańcuch z sąsiednim węzłem.
    """
    try:
        response = requests.get(f"{neighbor}/chain")
        neighbor_chain = response.json()
        if len(neighbor_chain) > len(blockchain.chain):
            blockchain.chain = [
                Block(
                    data=block["data"],
                    proof=block["proof"],
                    previous_hash=block["prev_hash"],
                    index=block["index"],
                    timestamp=block["timestamp"]
                )
                for block in neighbor_chain
            ]
            return {"message": "Blockchain synchronized successfully!"}
        else:
            return {"message": "Our chain is already up to date."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error syncing with neighbor: {str(e)}")