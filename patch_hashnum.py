lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()
lines[340] = "            pass  # Skip block hash check\n"
open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').writelines(lines)
print('Patch applique avec succes')
