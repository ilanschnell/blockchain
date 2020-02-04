The Blockchain
==============

Remarkable technology:
  - openness (anyone can see the chain)
  - distributed
  - permissionless (no access control)
  - resistant to modification of the data
  - secure

The first blockchain was conceptualized by Satoshi Nakamoto in 2008.

Ledger:

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
    | - A -> B  $3.56 |       |                 |       | - C -> C  $2.50 |
    +-----------------+       +-----------------+       +-----------------+


