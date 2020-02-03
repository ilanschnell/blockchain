from pprint import pprint

from blockchain import BlockChain


def test_blockchain():
    bc = BlockChain()
    for _ in range(2):
        bc.new_block()
    pprint(bc.chain)
    for i, block in enumerate(bc.chain):
        print(i, bc.hash(block))
    assert bc.valid_chain(bc.chain)


if __name__ == '__main__':
    test_blockchain()
