from pathlib import Path
from flask import Flask, jsonify, request
import requests
import sys

# Importy z Twojego kodu
from Blockchain.Blockchain import Blockchain

app = Flask(__name__)

# Każdy węzeł ma własną instancję Blockchain
blockchain = Blockchain()

# Zbiór adresów innych węzłów w sieci, np. "http://127.0.0.1:5001"
peers = set()


@app.route('/', methods=['GET'])
def home():
    """
    Prosta strona powitalna
    """
    return "Hello from your Blockchain Node!"


@app.route('/mine_block', methods=['POST'])
def mine_block():
    """
    Endpoint do 'kopania' nowego bloku z przesłanymi w żądaniu danymi.
    """
    data_json = request.get_json()
    if not data_json:
        return jsonify({"message": "No data provided"}), 400

    # Dla uproszczenia oczekujemy klucza "data" w JSON
    data = data_json.get('data', "No data")

    # Tworzymy nowy blok
    new_block = blockchain.mine_block(data=data)
    # Zwracamy informacje o nowym bloku
    return jsonify(new_block.toDictionary()), 200


@app.route('/chain', methods=['GET'])
def get_chain():
    """
    Zwraca cały aktualny łańcuch bloków w formacie JSON.
    """
    chain_data = [block.toDictionary() for block in blockchain.chain]
    response = {
        "length": len(chain_data),
        "chain": chain_data
    }
    return jsonify(response), 200


@app.route('/is_valid', methods=['GET'])
def is_valid():
    """
    Sprawdza, czy łańcuch jest poprawny.
    """
    valid = blockchain.validate_chain()
    response = {
        "is_valid": valid
    }
    return jsonify(response), 200


@app.route('/peers', methods=['GET'])
def get_peers():
    """
    Zwraca listę znanych węzłów (peers).
    """
    return jsonify(list(peers)), 200


@app.route('/register_node', methods=['POST'])
def register_node():
    """
    Dodaje nowy węzeł do listy znanych węzłów.
    Oczekuje w JSON klucza 'node_address', np. {"node_address": "http://127.0.0.1:5001"}
    """
    data_json = request.get_json()
    if not data_json:
        return jsonify({"message": "No data provided"}), 400

    node_address = data_json.get('node_address')
    if not node_address:
        return jsonify({"message": "No node_address field provided"}), 400

    peers.add(node_address)

    # Odpowiadamy listą wszystkich znanych węzłów
    return jsonify({
        "message": "New node added",
        "all_nodes": list(peers)
    }), 201


@app.route('/register_nodes_bulk', methods=['POST'])
def register_nodes_bulk():
    """
    Dodaje wiele nowych węzłów naraz.
    Oczekuje w JSON klucza 'nodes', np. {"nodes": ["http://127.0.0.1:5001", "http://127.0.0.1:5002"]}
    """
    data_json = request.get_json()
    if not data_json:
        return jsonify({"message": "No data provided"}), 400

    nodes = data_json.get('nodes')
    if not nodes:
        return jsonify({"message": "No nodes field provided"}), 400

    for node in nodes:
        peers.add(node)

    return jsonify({
        "message": "New nodes have been added",
        "all_nodes": list(peers)
    }), 201


@app.route('/sync_chain', methods=['GET'])
def sync_chain():
    """
    Próbuje zastąpić nasz łańcuch dłuższym (i poprawnym) łańcuchem od sąsiednich węzłów.
    """
    replaced = replace_chain()
    response = {
        "message": "Chain was replaced" if replaced else "No replacement was done",
        "chain": [block.toDictionary() for block in blockchain.chain]
    }
    return jsonify(response), 200


@app.route('/tamper_block', methods=['POST'])
def tamper_block():
    """
    UWAGA: Tylko do celów demonstracyjnych!!!
    Pozwala 'zepsuć' któryś blok i zobaczyć, że walidacja wykaże błąd.
    """
    data_json = request.get_json()
    if not data_json:
        return jsonify({"message": "No data provided"}), 400

    block_index = data_json.get("block_index")
    new_data = data_json.get("new_data")

    if block_index is None or new_data is None:
        return jsonify({"message": "Need block_index and new_data fields"}), 400

    # Zakładamy, że blockchain ma tyle bloków, żeby ten index istniał
    blockchain.chain[block_index].data = new_data

    return jsonify({"message": f"Block {block_index} was tampered with."}), 200


def replace_chain():
    """
    Przechodzi przez wszystkie węzły, pobiera od nich łańcuch i sprawdza,
    czy nie mają dłuższego (i ważnego) łańcucha niż my. Jeśli tak, to go przyjmujemy.
    Zwraca True, jeśli łańcuch został zastąpiony, w przeciwnym wypadku False.
    """
    global blockchain
    longest_chain = None
    max_length = len(blockchain.chain)

    for node in peers:
        try:
            response = requests.get(f"{node}/chain")
            if response.status_code == 200:
                data = response.json()
                length = data['length']
                chain_data = data['chain']

                if length > max_length:
                    # Tymczasowo stwórz nową instancję Blockchain i sprawdź validację
                    temp_chain = Blockchain()
                    temp_chain.chain = []  # Wyczyść i wypełnij ręcznie

                    # Odtwarzamy łańcuch z JSON
                    for block_json in chain_data:
                        temp_chain.chain.append(_json_to_block(block_json))

                    if temp_chain.validate_chain() and length > max_length:
                        max_length = length
                        longest_chain = temp_chain.chain
        except Exception as e:
            print(f"Could not connect to {node}. Error: {e}")

    if longest_chain:
        blockchain.chain = longest_chain
        return True

    return False


def _json_to_block(block_json):
    """
    Pomocnicza funkcja do odtwarzania obiektu Block z formatu JSON.
    """
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
    """
    Uruchamianie:
        python app.py 5000
    lub 
        python app.py
    aby domyślnie wystartować na porcie 5000
    """
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = 5000

    app.run(host='0.0.0.0', port=port)
