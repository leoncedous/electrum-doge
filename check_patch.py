content = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').read()
print("Longueur fichier:", len(content))
print("Pattern trouve:", "compute target from chunk x" in content)
