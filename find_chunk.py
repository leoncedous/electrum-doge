lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()
for i, line in enumerate(lines):
    if 'def verify_chunk' in line:
        print(f"Ligne {i}: {repr(line)}")
        for j in range(i, i+20):
            print(f"{j}: {repr(lines[j])}")
        break
