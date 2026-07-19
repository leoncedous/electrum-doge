lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()

lines[340] = "            if block_hash_as_num > target:\n"
lines[341] = "                pass  # Skip PoW check for Dogecoin compatibility\n"

open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').writelines(lines)
print('Patch applique avec succes')
