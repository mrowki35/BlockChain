from flask import Flask, jsonify, request
import requests
import sys
from Blockchain.Blockchain import Blockchain
from Handlers.CapitalTransactionHandler import CapitalTransactionHandler
from Handlers.DividendTransactionHandler import DividendTransactionHandler
from Handlers.StockTransactionHandler import StockTransactionHandler
from Handlers.VotingTransactionHandler import VotingTransactionHandler
from Handlers.save_handler import SaveHandler
from Logging.Logger import Logger
from Logging.SeverityEnum import Severity

app = Flask(__name__)

# Initialize logger
logger = Logger()

# Blockchain instance and peers set
blockchain = Blockchain()
peers = set()

stock_handler = StockTransactionHandler()
capital_handler = CapitalTransactionHandler()
dividend_handler = DividendTransactionHandler()
voting_handler = VotingTransactionHandler()
save_handler = SaveHandler()

stock_handler.set_next(capital_handler) \
    .set_next(dividend_handler) \
    .set_next(voting_handler)


@app.route('/', methods=['GET'])
def home():
    logger.log("Accessed home endpoint")
    return "Hello from your Blockchain Node!"


@app.route('/mine_block', methods=['POST'])
def mine_block():
    data_json = request.get_json()
    if not data_json:
        logger.warning("No data provided to /mine_block")
        return jsonify({"message": "No data provided"}), 400

    data = data_json.get('data', "No data")
    new_block = blockchain.mine_block(data=data)
    logger.log(f"Block mined successfully: {new_block.toDictionary()}")

    block_data = new_block.data

    if isinstance(block_data, dict):
        save_handler.save(stock_handler.handle(block_data))
    elif isinstance(block_data, list):
        for tx_data in block_data:
            save_handler.save(stock_handler.handle(tx_data))
    else:
        logger.log("No valid transaction data structure recognized")

    return jsonify(new_block.toDictionary()), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    chain_data = [block.toDictionary() for block in blockchain]
    logger.log(f"Returned blockchain with {len(chain_data)} blocks")
    return jsonify({"length": len(chain_data), "chain": chain_data}), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.validate_chain()
    logger.log(f"Blockchain validity checked: {valid}")
    return jsonify({"is_valid": valid}), 200


@app.route('/peers', methods=['GET'])
def get_peers():
    logger.log("Accessed peers endpoint")
    return jsonify(list(peers)), 200


@app.route('/register_node', methods=['POST'])
def register_node():
    data_json = request.get_json()
    if not data_json:
        logger.warning("No data provided to /register_node")
        return jsonify({"message": "No data provided"}), 400

    node_address = data_json.get('node_address')
    if not node_address:
        logger.warning("No node_address provided in /register_node")
        return jsonify({"message": "No node_address field provided"}), 400

    peers.add(node_address)
    logger.log(f"New node registered: {node_address}")
    return jsonify({"message": "New node added", "all_nodes": list(peers)}), 201


@app.route('/register_nodes_bulk', methods=['POST'])
def register_nodes_bulk():
    data_json = request.get_json()
    if not data_json:
        logger.warning("No data provided to /register_nodes_bulk")
        return jsonify({"message": "No data provided"}), 400

    nodes = data_json.get('nodes')
    if not nodes:
        logger.warning("No nodes field provided in /register_nodes_bulk")
        return jsonify({"message": "No nodes field provided"}), 400

    for node in nodes:
        peers.add(node)

    logger.log(f"Bulk registered nodes: {nodes}")
    return jsonify({"message": "New nodes have been added", "all_nodes": list(peers)}), 201


@app.route('/sync_chain', methods=['GET'])
def sync_chain():
    replaced = replace_chain()
    logger.log("Chain synchronization complete")

    for block in blockchain.chain:
        block_data = block.data
        if isinstance(block_data, dict):
            save_handler.save(stock_handler.handle(block_data))
        elif isinstance(block_data, list):
            for tx_data in block_data:
                save_handler.save(stock_handler.handle(tx_data))

    return jsonify({
        "message": "Chain was replaced" if replaced else "No replacement was done",
        "chain": [block.toDictionary() for block in blockchain.chain]
    }), 200


@app.route('/tamper_block', methods=['POST'])
def tamper_block():
    data_json = request.get_json()
    if not data_json:
        logger.warning("No data provided to /tamper_block")
        return jsonify({"message": "No data provided"}), 400

    block_index = data_json.get("block_index")
    new_data = data_json.get("new_data")
    if block_index is None or new_data is None:
        logger.warning("Missing fields in /tamper_block request")
        return jsonify({"message": "Need block_index and new_data fields"}), 400

    if block_index < 0 or block_index >= len(blockchain.chain):
        logger.warning(f"Block index {block_index} out of range")
        return jsonify({"message": "Block index out of range"}), 400

    original_block = blockchain.chain[block_index].clone()
    logger.log(f"Original block {block_index} cloned for backup: {original_block.toDictionary()}")

    blockchain.chain[block_index].data = new_data
    logger.warning(f"Block {block_index} tampered with: {new_data}")

    return jsonify({"message": f"Block {block_index} was tampered with."}), 200


def replace_chain():
    global blockchain
    longest_chain = None
    max_length = len(blockchain.chain)

    for node in peers:
        try:
            response = requests.get(f"{node}/get_chain")
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain_data = data['chain']
                logger.log(data)

                if length > max_length:
                    temp_chain = Blockchain()
                    temp_chain.chain = []

                    for block_json in chain_data:
                        temp_chain.chain.append(_json_to_block(block_json))

                    if temp_chain.validate_chain() and length > max_length:
                        max_length = length
                        longest_chain = temp_chain.chain

        except Exception as e:
            logger.error(f"Could not connect to {node}. Error: {e}", Severity.HIGH)

    if longest_chain:
        blockchain.chain = longest_chain
        logger.log("Blockchain replaced with longer valid chain")
        return True

    logger.log("No valid longer chain found")
    return False


def _json_to_block(block_json):
    from Blockchain.Block import Block
    block = Block(
        data=block_json["data"],
        proof=block_json["proof"],
        previous_hash=block_json["prev_hash"],
        index=block_json["index"],
        timestamp=block_json["timestamp"]
    )
    return block


if __name__ == "__main__":
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000

    logger.log(f"Starting Blockchain Node on port {port}")
    app.run(host='0.0.0.0', port=port)
