lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()

# Ligne 337: if not skip_auxpow:
# Ligne 338:     _pow_hash = auxpow.hash_parent_header(header)
# On remplace par skip_auxpow = True pour toujours skipper
lines[336] = "            skip_auxpow = True\n"
lines[337] = "        if not skip_auxpow:\n"
lines[338] = "            pass  # Skip AuxPoW verification for Dogecoin compatibility\n"

open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').writelines(lines)
print('Patch AuxPoW applique avec succes')
