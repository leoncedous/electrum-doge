lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'bits mismatch' in line:
        print(f"Ligne {i}: {repr(line)}")
        for j in range(max(0,i-5), i+5):
            print(f"{j}: {repr(lines[j])}")
        break
