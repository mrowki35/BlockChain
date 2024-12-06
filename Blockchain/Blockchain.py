from Block import Block
import datetime as dt
import hashlib
import json

class Blockchain:
    def __init__(self) -> None:
        self.chain=list()
        gen_block=None
        self.chain.append(gen_block)

    def createBlock(self, data, proof, prev_hash, index) -> Block:
        block = Block(data, proof, prev_hash, index, str(dt.datetime.now()))

    def getPreviuosBlock(self)-> Block:
        return self.chain[-1]
    
    def mineBlock(self, data:str) -> Block:
        prevBlock = self.getPreviuosBlock()
        prevProof = prevBlock.proof
        index = prevBlock.index 
        proof = self.proofOfWork(prevProof, index, data)
        previousHash=self.hashBlock(prevBlock)
        block = self.createBlock(data=data,proof=proof,prev_hash=previousHash,index=index)
        self.chain.append(block)
        return block

    def proofOfWork(self,prev_proof, index, data) -> int:
        new_proof = 1
        check_proof = False
        while not check_proof:
            to_dig = self.digest(new_proof,prev_proof,index,data)
            hash_value = hashlib.sha256(to_dig).hexdigest()
            if hash_value[:6] == "000000":
                check_proof = True
            else:
                new_proof+=1
        return new_proof
    
    def hashBlock(self, Block)->str:
        encoded_block = json.dumps(Block.toDictionary(), sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()

    def digest(self, new_proof, previous_proof, index, data) -> bytes:
        #algorithm calculating - > change this to be much more complex
        to_digest = str(new_proof ** 2- previous_proof**2 + index) + data
        return to_digest.encode()
    
    def validateChain(self) -> bool:
        currentBlock = self.chain[0]
        block_index = 1
        while block_index < len(self.chain):
            nextBlock = self.chain[block_index]
            if nextBlock.previous_hash != self.hash(currentBlock):
                return False
            currentProof = currentBlock.proof
            next_index, next_data , next_proof = (nextBlock.index,nextBlock.data,nextBlock.proof)
            hashValue = hashlib.sha256(self.digest(new_proof=next_proof,previous_proof=currentProof,index=next_index,data=next_data)).hexdigest()
            if hashValue [:4]!= "0000":
                return False
            currentBlock = nextBlock
            block_index+=1
        return True