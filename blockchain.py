# Blockchain example.  I made some modifications to the original code from:
# https://hackernoon.com/learn-blockchains-by-building-one-117428612f46
import json
import hashlib
from time import time
from pprint import pprint
from urllib.parse import urlparse

import requests
from flask import Flask, jsonify, request

genesis_block = {
    'index': 0,
    'nonce': 37783,
    'previous_hash': '<genesis: no previous hash>',
    'timestamp': 1580618745,
    'transactions': [],
}

class BlockChain(object):
    def __init__(self):
        self.current_transactions = []
        self.chain = [genesis_block]
        self.nodes = set()
        # Create the genesis block
        #self.new_block(previous_hash='<genesis: no previous hash>')

    def register_node(self, address):
        """
        Add a new node to the set of nodes
        :param address: Address of node. Eg. 'http://192.168.0.5:5000'
        """
        parsed_url = urlparse(address)
        if parsed_url.netloc:
            self.nodes.add(parsed_url.netloc)
        elif parsed_url.path:
            # Accepts an URL without scheme like '192.168.0.5:5000'.
            self.nodes.add(parsed_url.path)
        else:
            raise ValueError('Invalid URL')

    def valid_chain(self, chain):
        last_block = chain[0]
        current_index = 1

        while current_index < len(chain):
            block = chain[current_index]
            if block['previous_hash'] != self.hash(last_block):
                return False
            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        This is our consensus algorithm, it resolves conflicts
        by replacing our chain with the longest one in the network.
        :return: True if our chain was replaced, False if not
        """
        new_chain = None

        # We're only looking for chains longer than ours
        max_length = len(self.chain)

        # Grab and verify the chains from all the nodes in our network
        for node in self.nodes:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                # Check if the length is longer and the chain is valid
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        # Replace our chain if we discovered a new,
        # valid chain longer than ours
        if new_chain:
            self.chain = new_chain
            return True

        return False

    def new_block(self, previous_hash=None):
        if previous_hash is None:
            previous_hash = self.hash(self.chain[-1])

        block = {
            'index': len(self.chain),
            'timestamp': int(time()),
            'transactions': self.current_transactions,
            'nonce': 0,
            'previous_hash': previous_hash,
        }
        while self.hash(block)[0:4] != '0000':
            block['nonce'] += 1

        self.chain.append(block)

        # Reset the current list of transactions
        self.current_transactions = []

        return block

    def new_transaction(self, sender, recipient, amount):
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def hash(block):
        # We must make sure that the dictionary is sorted,
        # or we'll have inconsistent hashes
        assert isinstance(block, dict), block
        block_data = json.dumps(block, sort_keys=True).encode()
        return hashlib.sha256(block_data).hexdigest()


def test_blockchain():
    bc = BlockChain()
    for _ in range(2):
        bc.new_block()
    pprint(bc.chain)
    for i, block in enumerate(bc.chain):
        print(i, bc.hash(block))
    print(bc.valid_chain(bc.chain))


# Instantiate the Node
app = Flask(__name__)

node_id = None

# Instantiate the Blockchain
blockchain = BlockChain()


@app.route('/mine', methods=['GET'])
def mine():
    # We must receive a reward for finding the proof.
    # The sender is "0" to signify that this node has mined a new coin.
    blockchain.new_transaction(
        sender = "0",
        recipient = node_id,
        amount = 1,
    )

    block = blockchain.new_block()  # mine a new Block

    response = {
        'message': "new block mined",
        'index': block['index'],
        'transactions': block['transactions'],
        'previous_hash': block['previous_hash'],
    }
    return jsonify(response), 200

@app.route('/transactions/new', methods=['POST'])
def new_transaction():
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new Transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'],
                                       values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201

@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200

@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    values = request.get_json()

    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list of nodes", 400

    for node in nodes:
        blockchain.register_node(node)

    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201

@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    replaced = blockchain.resolve_conflicts()

    if replaced:
        response = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        response = {
            'message': 'Our chain is authoritative',
            'chain': blockchain.chain
        }
    return jsonify(response), 200

if __name__ == '__main__':
    from argparse import ArgumentParser

    parser = ArgumentParser()
    parser.add_argument('id', metavar='ID', type=str, nargs=1,
                    help='node id')
    parser.add_argument('-p', '--port', default=5000,
                        type=int, help='port to listen on')
    args = parser.parse_args()
    node_id = args.id[0]
    print(f'{node_id=}')
    port = args.port

    app.run(host='0.0.0.0', port=port)
