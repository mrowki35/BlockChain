import requests
from flask import Flask, jsonify, request
from Blockchain.Blockchain import Blockchain
from Blockchain.Block import Block

app = Flask(__name__)

# Tworzymy instancję blockchain
blockchain = Blockchain()

@app.route("/chain", methods=["GET"])
def get_chain():
    """
    Zwraca cały łańcuch bloków.
    """
    chain = [block.toDictionary() for block in blockchain.chain]
    return jsonify(chain), 200

@app.route("/mine", methods=["POST"])
def mine_block():
    """
    Tworzy nowy blok z podanymi danymi.
    """
    data = request.json.get("data", None)
    if not data:
        return jsonify({"error": "No data provided"}), 400

    new_block = blockchain.mine_block(data)
    return jsonify({"message": "Block mined successfully!", "block": new_block.toDictionary()}), 201

@app.route("/validate", methods=["GET"])
def validate_chain():
    """
    Sprawdza, czy łańcuch jest poprawny.
    """
    is_valid = blockchain.validate_chain()
    if is_valid:
        return jsonify({"message": "Blockchain is valid!"}), 200
    else:
        return jsonify({"error": "Blockchain is invalid!"}), 400

@app.route("/add_block", methods=["POST"])
def add_block():
    """
    Dodaje blok do łańcucha (synchronizacja między węzłami).
    """
    block_data = request.json
    try:
        new_block = Block(
            data=block_data["data"],
            proof=block_data["proof"],
            previous_hash=block_data["previous_hash"],
            index=block_data["index"],
            timestamp=block_data["timestamp"]
        )
        previous_block = blockchain.get_previous_block()

        if new_block.previous_hash != blockchain.hash_block(previous_block):
            return jsonify({"error": "Previous hash does not match!"}), 400

        if not blockchain.proof_of_work(previous_block.proof, new_block.index, new_block.data) == new_block.proof:
            return jsonify({"error": "Proof of work is invalid!"}), 400

        blockchain.chain.append(new_block)
        return jsonify({"message": "Block added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sync", methods=["POST"])
def sync_chain():
    """
    Synchronizuje łańcuch z sąsiednim węzłem.
    """
    neighbor = request.json.get("neighbor", None)
    if not neighbor:
        return jsonify({"error": "No neighbor URL provided"}), 400

    try:
        response = requests.get(f"{neighbor}/chain")
        if response.status_code == 200:
            neighbor_chain = response.json()
            if len(neighbor_chain) > len(blockchain.chain):
                blockchain.chain = [
                    Block(
                        data=block["data"],
                        proof=block["proof"],
                        previous_hash=block["previous_hash"],
                        index=block["index"],
                        timestamp=block["timestamp"]
                    )
                    for block in neighbor_chain
                ]
                return jsonify({"message": "Blockchain synchronized successfully!"}), 200
            else:
                return jsonify({"message": "Our chain is already up to date."}), 200
        else:
            return jsonify({"error": "Failed to fetch chain from neighbor!"}), response.status_code
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)
