lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'AuxPoW' in line or 'auxpow' in line.lower():
        print(f"{i}: {repr(line)}")
