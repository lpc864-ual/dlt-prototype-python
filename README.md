# Simple DLT (Blockchain) Prototype with Python

This project implements a simple Distributed Ledger Technology (DLT) prototype based on blockchain, including proof of work, append operation, and a timestamp system.

## Features

- **Proof of Work (PoW)**: Blocks require a hash with a specific number of leading zeros
- **Immutable Chain**: Each block links to the previous one using cryptographic hashes
- **Timestamp System**: All blocks and transactions include timestamps
- **Transaction Pool**: Pending transactions are stored and included in the next block
- **Chain Validation**: Functions to verify the integrity of the entire blockchain

## Requirements

- Python 3.6 or higher
- No external dependencies required (only standard library)

## Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/dlt-prototype-python.git
cd dlt-prototype-python
```

No additional installation is required.

## Usage

Run the demo:

```bash
py app.py
```

## Understanding the Code

### Block Structure

Each block contains:
- `index`: Position in the chain
- `previous_hash`: Hash of the previous block
- `timestamp`: When the block was created
- `data`: Transactions or other information
- `nonce`: Value used for proof of work
- `hash`: The block's own hash

### Blockchain Operations

The main operations are:
- `add_transaction()`: Add a transaction to the pending pool
- `append_block()`: Create a new block and add it to the chain
- `mine_block()`: Find a valid hash for a block (proof of work)
- `is_chain_valid()`: Verify the integrity of the entire chain

### Using the blockchain in your own code

```python
from blockchain import Blockchain, Block

# Create a new blockchain with difficulty level 3
my_blockchain = Blockchain(difficulty=3)

# Add a transaction to the pending pool
my_blockchain.add_transaction({
    "from": "Alice", 
    "to": "Bob", 
    "amount": 50
})

# Create a new block with all pending transactions
new_block = my_blockchain.append_block()

# Create a block with custom data
custom_block = my_blockchain.append_block({
    "message": "This is a custom block"
})

# Verify the blockchain's integrity
is_valid = my_blockchain.is_chain_valid()
print(f"Is blockchain valid? {is_valid}")

# Print the entire blockchain
my_blockchain.print_chain()
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.