content = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').read()

new_method = """
    def get_target_digishield(self, height: int) -> int:
        # DigiShield per-block difficulty for Dogecoin
        last = self.read_header(height)
        if not last:
            raise MissingHeader()
        prev = self.read_header(height - 1)
        if not prev:
            raise MissingHeader()
        bits = last.get('bits')
        target = self.bits_to_target(bits)
        nActualTimespan = last.get('timestamp') - prev.get('timestamp')
        nTargetTimespan = 60
        nActualTimespan = max(nActualTimespan, nTargetTimespan - nTargetTimespan // 4)
        nActualTimespan = min(nActualTimespan, nTargetTimespan + nTargetTimespan // 4)
        new_target = min(MAX_TARGET, (target * nActualTimespan) // nTargetTimespan)
        new_target = self.bits_to_target(self.target_to_bits(new_target))
        return new_target
"""

# Insert after get_target method
insert_after = "            new_target = self.bits_to_target(self.target_to_bits(new_target))\n            return new_target\n    @classmethod\n    def bits_to_target"
replacement = "            new_target = self.bits_to_target(self.target_to_bits(new_target))\n            return new_target\n" + new_method + "\n    @classmethod\n    def bits_to_target"

if insert_after in content:
    content = content.replace(insert_after, replacement)
    open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').write(content)
    print('get_target_digishield ajoute avec succes')
else:
    print('Pattern non trouve')
