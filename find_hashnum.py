lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'block_hash_as_num' in line:
        print(f"{i}: {repr(line)}")
