# The Blockchain


## Remarkable technology:
  - openness (anyone can see the chain)
  - distributed and decentral
  - permissionless (no access control)
  - resistant to modification of the data
  - redundant
  - secure


### blockchain = open, distributed, database
  - in case of cryptocurrencies the data are monetary transactions
  - a private blockchain is just a (overly sophisticated) database


The first blockchain was conceptualized by Satoshi Nakamoto in 2008.

## Ledger:

    +-----------------+       +-----------------+       +-----------------+
    | Genesis Block   |       | Block 1         |       | Block 2         |
    | - previous hash | ----> | - previous hash | ----> | - previous hash |
    | - timestamp     |       | - timestamp     |       | - timestamp     |
    | - nonce         |       | - nonce         |       | - nonce         |
    | - Merkle hash   |       | - Merkle hash   |       | - Merkle hash   |
    +-----------------+       +-----------------+       +-----------------+
            ^                         ^                         ^
            |                         |                         |
    +-----------------+       +-----------------+       +-----------------+
    | Transactions:   |       | Transactions:   |       | Transactions:   |
    | - A -> B $73.87 |       | - B -> C $12.55 |       | - A -> D  $3.00 |
    | - A -> B  $3.56 |       +-----------------+       | - C -> C  $2.50 |
    +-----------------+                                 | - B -> C $17.24 |
                                                        +-----------------+


## Each node has a copy of the ledger:

<img src="./decentralized-network.png" width="304" height="273" />


## Timeline of a transaction:
  - a transaction is agreed upon
  - transaction is broadcasted
  - nodes verify transaction
  - some node will "mine" a block (which links to all outstanding transactions)
  - block is now part of the chain


## Consensus (longest chain wins):

<img src="./chain.svg" width="153" height="406" />
