## Dump Bitcoin addresses with positive balance

Simple utility to list all bitcoin addresses with positive balance. It works by analysing the current unspent transaction output set (UTXO), 
aggregating outputs to same addresses together and write them to csv file.

#### Prequisities:  
python 2.7  
pip  

#### To install:  
run pip install -r requirements.txt

or install following packages with pip manualy
* hashlib
* plyvel
* base58
* sqlite3

#### Usage
To use you will need copy of chainstate database as created by [bitcoin core](https://bitcoin.org/en/bitcoin-core/)
 client. I've not tried different clients.
 
To get current addresses with positive balance, let the full node client sync with the network. 
**Stop** the bitcoin-core client before running this utility. If you not stop the client, the database might get corrupted.  
Then run this program with path to chainstate directory (usualy $HOME/.bitcoin/chainstate).

Show help
```
python dump.py -h
```
#### Example:  
Following will read from `/home/USER/.bitcoin/chainstate`, and write result to `/home/USER/addresses_with_balance.csv`.
```
python dump.py /home/USER/.bitcoin/chainstate /home/USER/addresses_with_balance.csv
```

##### Notice
* That the output may not be complete as there are some transactions which are not understood by the decoding lib, or that which do not have "address" at all. Such transactions are not processed. Number of them and the total ammount is displayed after the analysis.  
* The output csv file only reflects the chainstate leveldb at your disk. So it will always be few blocks behind the network as you need to stop the bitcoin-core client.

#### Converting to RIPEMD160
```
python convert2ripemd160.py /home/USER/addresses_with_balance.csv
```
#### Converting to RIPEMD160 Python SET

```
python csv_to_hash160_set.py

```

