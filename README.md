# Blockchain

A basic blockchain implementation with multiple clients, transaction handlers, and chain synchronization features.

---

## Table of Contents

1. [Overview](#overview)
2. [Features](#features)
3. [Technologies used](#technologies-used)
4. [Project structure](#project-structure)
5. [Pre-requisites](#pre-requisites)
6. [How to run the project](#how-to-run-the-project)
    - [Starting a node](#starting-a-node)
    - [Register peers](#register-peers)
    - [Mining a block](#mining-a-block)
    - [Syncing chains](#syncing-chains)
    - [Tampering with a block](#tampering-with-a-block)
    - [Validate the blockchain](#validate-the-blockchain)
7. [Testing the project](#testing-the-project)
8. [Advanced Features](#advanced-features)
9. [Contributors](#contributors)
10. [License](#license)

---

## Overview

This project implements a basic blockchain system with multiple clients, transaction handlers, and chain synchronization
features. The blockchain supports transaction validation, block mining, and peer-to-peer synchronization between nodes.
It includes features like prototype pattern usage, chain of responsibility for transaction handling, and tamper-proof
chain validation.

---

## Features

- **Blockchain Basics**: Genesis block, proof-of-work, block validation.

- **Transactions**: Support for multiple transaction types (e.g., buying shares, selling shares, dividend payments).

- **Chain Synchronization**: Peer-to-peer synchronization to ensure nodes have the longest valid chain.

- **Prototype Pattern**: Cloning of blocks and transactions.

- **Chain of Responsibility**: Modular handlers for transaction validation and processing.

- **Logging**: Comprehensive logging for debugging and monitoring.

---

## Technologies used

- **Python**: Core implementation.

- **Flask**: REST API framework.

- **JSON**: Data serialization and communication between nodes.

- **Requests**: HTTP requests for peer-to-peer communication.

- **Unittest**: Unit testing framework.

---

## Project structure

```plaintext
blockchain_project/
├── Blockchain/
│   ├── Blockchain.py        # Core blockchain logic
│   ├── Block.py             # Block structure and functionality
│   ├── BlockBuilder.py      # Builder pattern for block creation
├── Handlers/
│   ├── StockTransactionHandler.py  # Handler for stock-related transactions
│   ├── CapitalTransactionHandler.py # Handler for capital-related transactions
│   ├── DividendTransactionHandler.py # Handler for dividend transactions
│   ├── TransactionHandler.py # Defines a concrete class TransactionHandler that processes transactions and passes them to the next handler in the chain if it exists.
│   ├── GeneralValidationHandler.py # Handler for general transaction validation, used in Unit tests
│   ├── ExecutionHandler.py  # ExectutionHandler for executing transactions, used in Unit tests
│   ├── save_handler.py      # SaveHandler for saving blocks and transactions
│   ├── base_handler.py      # Abstract base class for handlers
├── Logging/
│   ├── Logger.py            # Logging utility
│   ├── SeverityEnum.py      # Severity levels for logging
├── Transactions/
│   ├── Transaction.py       # Abstract base class for transactions
│   ├── AbstractTransactionFactory.py # Abstract factory for creating transactions
│   ├── BuyingSharesTransaction.py  # Transaction for buying shares
│   ├── CapitalTranscationFactory.py # Factory for creating capital-related transactions, used in Unit tests
│   ├── DividendFactory.py   # Factory for creating dividend transactions
│   ├── GrantingStocksTransaction.py # Transaction for granting stocks
│   ├── IncreasingCapitalTransaction.py # Transaction for increasing capital
│   ├── IssuingStocksTransaction.py # Transaction for issuing stocks
│   ├── SellingSharesTransaction.py # Transaction for selling shares
│   ├── PayingDividendsTransaction.py # Transaction for paying dividends
│   ├── StockTransactionFactory.py  # Factory for creating stock-related transactions
│   ├── VotingResultsTransaction.py # Transaction for voting, used in Unit tests
│   ├── VotingTransactionFactory.py # Factory for creating voting transactions, used in Unit tests

├── app.py                   # Main Flask application
├── tests/
│   ├── BlockchainTest.py    # Unit tests for blockchain
│   ├── TestHandlers.py       # Unit tests for handlers
│   ├── TestBlockchainTransactions.py  # Unit tests for transactions
│   ├── LoggerTest.py        # Unit tests for logging
│   ├── TestCapitalTransaction.py # Unit tests for capital transaction 
│   ├── TestVotingTransaction.py # Unit tests for voting transaction



├── requirements.txt         # Python dependencies
└── README.md                # Project documentation
```

---

## Pre-requisites

1. **Python**: Version 3.8 or higher.

2. **Pip**: Python package manager.

Install required dependencies:

```bash
pip install -r requirements.txt
```

---

## How to run the project

### Starting a node

1. Start the Flask app on a specific port:

   ```bash
   python app.py <port_number>
   ```

   Example:

   ```bash
   python app.py 5000
   ```

2. Start additional nodes on different ports:

    ```bash
    python app.py 5001
    python app.py 5002
   python app.py 5003
    ```

### Register peers

Use the `/register_node` endpoint to link nodes together:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"node_address": "http://127.0.0.1:5001"}' \
http://127.0.0.1:5000/register_node
```

Repeat for other nodes.

### Mining a block

Submit a transaction and mine a block:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"data": {"transaction_type": "SELLING_SHARES", "seller": "Alice", "buyer": "Bob", "shares": 50, "price": 100.0}}' \
http://127.0.0.1:5000/mine_block
```

### Syncing chains

Trigger chain synchronization across peers:

```bash
curl http://127.0.0.1:5001/sync_chain
```

### Tampering with a block

Manually modify a block to test validation:

```bash
curl -X POST -H "Content-Type: application/json" \
-d '{"block_index": 1, "new_data": "tampered data"}' \
http://127.0.0.1:5000/tamper_block
```

### Validate the blockchain

Check if the blockchain is valid:

```bash
curl http://127.0.0.1:5000/is_valid
```

---

## Testing the project

Run unit tests using the unittest framework:

```bash
python -m unittest discover -s tests
```

### Example Edge Cases

1. **Invalid transaction data**:
    - Missing required fields (e.g., `seller` or `buyer` in a transaction).
    - Negative values for `shares` or `price`.

2. **Tampered block**:
    - Use `/tamper_block` to modify a block and check validation results.

3. **Multiple clients**:
    - Test synchronization with nodes at different stages of the blockchain.

4. **Large block**:
    - Submit multiple transactions in one block and validate consistency.

5. **Prototype pattern**:
    - Clone transactions or blocks and validate their independence.

---

## Advanced Features

1. **Chain of Responsibility**: Modular handlers for processing transactions.

2. **Prototype Pattern**: Use the `clone()` method to create independent copies of blocks or transactions.

3. **SaveHandler**: Automatically saves processed blocks and transactions to files for persistence.

---

## Contributors

- [Maciej Michałek](https://github.com/McMichalek)
- [Arkadiusz Mika](https://github.com/Arkadiusz4)
- [Przemysław Orlikowski](https://github.com/mrowki35)
- [Gabriela Czapska]()

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.