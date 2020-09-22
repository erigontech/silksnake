# Silksnake command-line tools

The [tools](../tools) folder contains a set of simple command-line utilities for interacting with Turbo-Geth/Silkworm key-value store by means of their
[gRPC](https://grpc.io/) Key-Value (KV) interface. The examples are taken using a Turbo-Geth node synced with [Goerli](https://goerli.net/) testnet.

## __kv_seek__

This is the lowest level command: a simple wrapper around gRPC KV seek message.

```shell-session
$ ./tools/kv_seek.py -h
usage: kv_seek.py [-h] [-t TARGET] bucket seek_key

The kv_seek command allows to query the turbo-geth/silkworm KV gRPC.

positional arguments:
bucket                the bucket tag as string
seek_key              the seek key as hex string without leading 0x

optional arguments:
-h, --help            show this help message and exit
-t TARGET, --target TARGET
                        the server location as string <address>:<port>
```

At completion kv_seek prints a __REQ__ section containing the provided parameters just for check and a __RSP__ section with:

- __key__: the complete key of the result associated with seek key (if any)
- __value__: the value of the result associated with seek key (if any)

Both key and value can be empty if no match is found.

Let's see an example for bucket __Block Bodies__ (string label: _b_) and seek_key equal to block number __3384027__ (8-byte big-endian: _000000000033a2db_):

```shell-session
$ ./tools/kv_seek.py b 000000000033a2db
REQ bucket: b seek_key: 000000000033a2db
RSP key: 000000000033a2db05d7db38db2cecdc2a195159a02530b69b47d0ec970d5275352870769d94a618 value: c2c0c0
```

The command outputs the key corresponding to the concatenation of the block number (000000000033a2db) with the block hash (0x05d7db38db2cecdc2a195159a02530b69b47d0ec970d5275352870769d94a618). You can check by yourself [here](https://goerli.etherscan.io/block/3384027).

BTW this is an empty block (sometimes happens), hence the value _c2c0c0_ as block body (see [RLP](https://eth.wiki/fundamentals/rlp) for more info).

## __kv_seek_block_body__

```shell-session
$ ./tools/kv_seek_block_body.py -h
usage: kv_seek_block_body.py [-h] [-t TARGET] block_number

The kv_seek_block_body command allows to query the turbo-geth/silkworm KV 'Block Bodies' bucket.

positional arguments:
  block_number                  the block number as integer

optional arguments:
  -h, --help                    show this help message and exit
  -t TARGET, --target TARGET    the server location as string <address>:<port>
```

```shell-session
$ ./tools/kv_seek_block_body.py 3384025
REQ block_number: 3384025
RSP block_hash: c8caaa2831cc2e9b7710af3455e4d5a121ee7ba2d1d4293b69b4e8aeaed7309c transactions(1): [
Transaction(nonce=2406, gas_price=1000000, gas_limit=235255, to='12b731d23993eb97ba19e7c48ea6428edfd3e3e1', value=0, data='6a791f110000000000000000000000000000000000000000000000000000000000000040000000000000000000000000000000000000000000000000000000000000012000000000000000000000000000000000000000000000000000000000000000c0000000000000000000000000485afa8808deb85c07c1dcbc896623f67e2e763600000000000000000000000000000000000000000000000000000000000965360000000000000000000000000000000000000000000000000000000000096635c00fdd12a308538d70ee5ab0afef1e99d2281829f4063e767db281a28e601c92410d3bda2a1104a029442fd2e40400a42f5090c5681e0e4af34eb43201a85cbb000000000000000000000000000000000000000000000000000000000000ea610000000000000000000000000000000000000000000000000000000000000041bd7ce28a81a7f6568b22fcfded6ce60c19bf9aee8a78431640d3eb25b2df54f1279ce6fd6c0224075f68d547a1100a6a394c9ae1e29e145abd2df1e4b6eaccc80100000000000000000000000000000000000000000000000000000000000000', v=28, r=75558478713322080996021662556958317002460073864827931358726028031984324259798, s=13690458676460707975891026052172047103357432302662499481758076794019836483521)
] uncles(0): [
]
```

## __kv_seek_block_header__

```shell-session
$ ./tools/kv_seek_block_header.py -h
usage: kv_seek_block_body.py [-h] [-t TARGET] block_number

The kv_seek_block_header command allows to query the turbo-geth/silkworm KV 'Block Bodies' bucket.

positional arguments:
  block_number                  the block number as integer

optional arguments:
  -h, --help                    show this help message and exit
  -t TARGET, --target TARGET    the server location as string <address>:<port>
```

```shell-session
$ ./kv_seek_block_header.py 3384025
CANONICAL HEADER
REQ1 block_number: 3384025 (k1: 000000000033a2d96e)
RSP1 block_hash: c8caaa2831cc2e9b7710af3455e4d5a121ee7ba2d1d4293b69b4e8aeaed7309c 

FULL HEADER
REQ2 block_number: 3384025 (k2: 000000000033a2d9c8caaa2831cc2e9b7710af3455e4d5a121ee7ba2d1d4293b69b4e8aeaed7309c)
RSP2 block_header: (parent_hash='8dd83d9290cdd6067f5181ae478ab09273787de931627760e2ec1302e65b8c3d', uncles_hash='1dcc4de8dec75d7aab85b567b6ccd41ad312451b948a7413f0a142fd40d49347', coinbase='0000000000000000000000000000000000000000', state_root='b4903c34713723ab4947721926ec71d68632c97a01483b14eff3c00cd9dd6ae1', transaction_root='2eaaef3345abac42a8a8b69cc3aba9ed048ff574597b28892f9a1aca4811d7cf', receipt_root='a6b7e90455d5cf126684e2ffe4a542ff468e35f399f6db910a1ce4a7b9273bcb', bloom=20593584385689566374772843940890773563020353394947984553867702777774290393225683507386042330260078973025199126555670093901573833319797561397046904292683020111961084665153483807934133688650117123410948565251454819816403114192060617899070397573079200040873228999164088756947895629084176794484850092313200229387871110383982722488513905054815820025645826417712037487245600843532721973645985234208657525824488550656720319236260486018685587697006253959805955307540581587404086117063550932515227371486230706836035484718284464081809250440603215433322618260745072148480, difficulty=1, block_number=3384025, gas_limit=8000000, gas_used=224534, timestamp=1599828035, extra_data='726f6e696e6b61697a656e000000000000000000000000000000000000000000f2a1d12d1e6511c09634406e95ccfb6c2d9bfef5746f9f7157b294a0bbc7ed7c26a2840e1f033642575f59caeffb72f5d09d904cbfe041aaa73b801b88dabdf501', mix_hash='0000000000000000000000000000000000000000000000000000000000000000', nonce='0000000000000000') 

DIFFICULTY HEADER
REQ3 block_number: 3384025 (k3: 000000000033a2d9c8caaa2831cc2e9b7710af3455e4d5a121ee7ba2d1d4293b69b4e8aeaed7309c74)
RSP3 block_total_difficulty: 4933005
```

## __kv_seek_block_number__

```shell-session
$ ./kv_seek_block_number.py -h
usage: kv_seek_block_number.py [-h] [-t TARGET] block_hash

The kv_seek_block_number command allows to query the turbo-geth/silkworm KV 'Header Numbers' bucket.

positional arguments:
  block_hash                    the block hash as string (w or w/o 0x prefix)

optional arguments:
  -h, --help                    show this help message and exit
  -t TARGET, --target TARGET    the server location as string <address>:<port>
```

```shell-session
tullio@precision-5520:~/workspace/silksnake/tools$ ./kv_seek_block_number.py e42335922909e0d371ca5e0aeb78afacfb9ff7e073304f7b9da88344dfb15550
REQ block_hash: e42335922909e0d371ca5e0aeb78afacfb9ff7e073304f7b9da88344dfb15550
RSP block_number: 3384020 (000000000033a2d4)
```

## __kv_seek_block_receipt__

```shell-session
$ ./kv_seek_block_receipt.py -h
usage: kv_seek_block_receipt.py [-h] [-c COUNT] [-t TARGET] block_number

The kv_seek_block_receipt command allows to query the turbo-geth/silkworm KV 'Receipts' bucket.

positional arguments:
  block_number                  the block number as integer

optional arguments:
  -h, --help                    show this help message and exit
  -c COUNT, --count COUNT       the number of blocks to seek as integer
  -t TARGET, --target TARGET    the server location as string <address>:<port>
```

```shell-session
$ ./kv_seek_block_receipt.py 3384025
CANONICAL HEADER
REQ1 block_number: 3384025 (k1: 000000000033a2d96e)
RSP1 block_hash: c8caaa2831cc2e9b7710af3455e4d5a121ee7ba2d1d4293b69b4e8aeaed7309c 

RECEIPT
REQ2 block_number: 3384025 (k2: 000000000033a2d9c8caaa2831cc2e9b7710af3455e4d5a121ee7ba2d1d4293b69b4e8aeaed7309c)
RSP2 block_receipts(1): [
receipt#0 (status=1, cumulative_gas_used=224534, logs=((address='12b731d23993eb97ba19e7c48ea6428edfd3e3e1', topics=(84296055546980476430285673802279178496784999664957386893553175854702533784871, 413076226928859296260450102926706283730929874486, 24070000, 20188000000000000000000), data='00000000000000000000000000000000000000000000000000000000000965360000000000000000000000000000000000000000000000000000000000096635c00fdd12a308538d70ee5ab0afef1e99d2281829f4063e767db281a28e601c92'),))
]
```

## __kv_seek_plain_state__

```shell-session
$ ./kv_seek_plain_state.py -h
usage: kv_seek_plain_state.py [-h] [-l LOCATION] [-t TARGET] account_address

The kv_seek_plain_state command allows to query the turbo-geth/silkworm KV 'Plain State' bucket.

positional arguments:
  account_address                     the account address as hex string (w or w/o 0x prefix)

optional arguments:
  -h, --help                          show this help message and exit
  -l LOCATION, --location LOCATION    the storage location as hex string (w or w/o 0x prefix)
  -t TARGET, --target TARGET          the server location as string <address>:<port>
```

```shell-session
$ ./kv_seek_plain_state.py 256b4f8185caa65ea98764e8ea2fd9cd4a5993e6 -l 0x02
REQ1 account_address: 256b4f8185caa65ea98764e8ea2fd9cd4a5993e6
RSP1 account: (nonce=1, balance=0, incarnation=1, storage_root='', code_hash='10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c')
REQ2 storage_location: 0x02
RSP2 storage value: 7753cfad258efbc52a9a1452e42ffbce9be486cb

$ ./kv_seek_plain_state.py 256b4f8185caa65ea98764e8ea2fd9cd4a5993e6 -l 0x2
REQ1 account_address: 256b4f8185caa65ea98764e8ea2fd9cd4a5993e6
RSP1 account: (nonce=1, balance=0, incarnation=1, storage_root='', code_hash='10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c')
REQ2 storage_location: 0x2
RSP2 storage value: 7753cfad258efbc52a9a1452e42ffbce9be486cb

$ ./kv_seek_plain_state.py 256b4f8185caa65ea98764e8ea2fd9cd4a5993e6 -l 2
REQ1 account_address: 256b4f8185caa65ea98764e8ea2fd9cd4a5993e6
RSP1 account: (nonce=1, balance=0, incarnation=1, storage_root='', code_hash='10b37de11f39e0a372615c70e1d4d7c613937e8f61823d59be9bea62112e175c')
REQ2 storage_location: 2
RSP2 storage value: 7753cfad258efbc52a9a1452e42ffbce9be486cb

```
