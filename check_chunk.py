content = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').read()
idx = content.find('def verify_chunk')
print(repr(content[idx:idx+500]))
