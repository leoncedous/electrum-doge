lines = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').readlines()

# Ajouter le recalcul DigiShield apres la ligne "height = start_height + i" (ligne 351)
new_lines = []
for i, line in enumerate(lines):
    new_lines.append(line)
    if i == 351:  # apres "height = start_height + i"
        new_lines.append('            # DigiShield: recalculate target per block after 145000\n')
        new_lines.append('            if height >= 145000 and i > 0:\n')
        new_lines.append('                try:\n')
        new_lines.append('                    prev_header = self.read_header(height - 1)\n')
        new_lines.append('                    if prev_header:\n')
        new_lines.append('                        bits = prev_header.get("bits")\n')
        new_lines.append('                        tgt = self.bits_to_target(bits)\n')
        new_lines.append('                        nActualTimespan = prev_header.get("timestamp", 60)\n')
        new_lines.append('                        prev2 = self.read_header(height - 2)\n')
        new_lines.append('                        if prev2:\n')
        new_lines.append('                            nActualTimespan = prev_header.get("timestamp") - prev2.get("timestamp")\n')
        new_lines.append('                        nTargetTimespan = 60\n')
        new_lines.append('                        nActualTimespan = max(nActualTimespan, nTargetTimespan - nTargetTimespan // 4)\n')
        new_lines.append('                        nActualTimespan = min(nActualTimespan, nTargetTimespan + nTargetTimespan // 4)\n')
        new_lines.append('                        target = min(MAX_TARGET, (tgt * nActualTimespan) // nTargetTimespan)\n')
        new_lines.append('                        target = self.bits_to_target(self.target_to_bits(target))\n')
        new_lines.append('                except Exception:\n')
        new_lines.append('                    pass\n')

open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').writelines(new_lines)
print('Patch applique avec succes')
