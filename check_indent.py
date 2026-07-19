lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()
for i in range(335, 350):
    print(f"{i}: {repr(lines[i])}")
