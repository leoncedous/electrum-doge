content = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').read()

old = """    def get_target(self, index: int) -> int:
        # compute target from chunk x, used in chunk x+1
        if constants.net.TESTNET:
            return 0
        if index == -1:
            return MAX_TARGET
        if index < len(self.checkpoints):
            h, t = self.checkpoints[index]
            return t
        # new target
        if (index * 240 + 239 > 371337) and (index * 240 + 239 + 1 > 240):
            # Dogecoin: Apply retargeting hardfork after AuxPoW start
            first = self.read_header(index * 240 - 1)
        else:
            first = self.read_header(index * 240)
        last = self.read_header(index * 240 + 239)
        if not first or not last:
            raise MissingHeader()
        bits = last.get('bits')
        target = self.bits_to_target(bits)
        nActualTimespan = last.get('timestamp') - first.get('timestamp')
        nTargetTimespan = 4 * 60 * 60
        nActualTimespan = max(nActualTimespan, nTargetTimespan // 4)
        nActualTimespan = min(nActualTimespan, nTargetTimespan * 4)
        new_target = min(MAX_TARGET, (target * nActualTimespan) // nTargetTimespan)
        # not any target can be represented in 32 bits:
        new_target = self.bits_to_target(self.target_to_bits(new_target))
        return new_target"""

new = """    def get_target(self, index: int) -> int:
        # Dogecoin DigiShield difficulty adjustment
        if constants.net.TESTNET:
            return 0
        if index == -1:
            return MAX_TARGET
        if index < len(self.checkpoints):
            h, t = self.checkpoints[index]
            return t
        last_height = index * 240 + 239
        last = self.read_header(last_height)
        if not last:
            raise MissingHeader()
        if last_height < 145000:
            if (last_height > 371337) and (last_height + 1 > 240):
                first = self.read_header(index * 240 - 1)
            else:
                first = self.read_header(index * 240)
            if not first:
                raise MissingHeader()
            bits = last.get('bits')
            target = self.bits_to_target(bits)
            nActualTimespan = last.get('timestamp') - first.get('timestamp')
            nTargetTimespan = 4 * 60 * 60
            nActualTimespan = max(nActualTimespan, nTargetTimespan // 4)
            nActualTimespan = min(nActualTimespan, nTargetTimespan * 4)
            new_target = min(MAX_TARGET, (target * nActualTimespan) // nTargetTimespan)
            new_target = self.bits_to_target(self.target_to_bits(new_target))
            return new_target
        else:
            prev = self.read_header(last_height - 1)
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
            return new_target"""

if old in content:
    content = content.replace(old, new)
    open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').write(content)
    print('Patch applique avec succes')
else:
    print('Pattern non trouve')
