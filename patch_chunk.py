content = open('electrum_doge/electrum/blockchain.py', 'r', encoding='utf-8').read()

old = """    def verify_chunk(self, index: int, data: bytes) -> bytes:
        stripped = bytearray()
        start_position = 0
        start_height = index * 240
        prev_hash = self.get_hash(start_height - 1)
        target = self.get_target(index-1)
        i = 0
        while start_position < len(data):
            height = start_height + i
            try:
                expected_header_hash = self.get_hash(height)
            except MissingHeader:
                expected_header_hash = None
            # Strip auxpow header for disk
            stripped.extend(data[start_position:start_position+HEADER_SIZE])
            header, start_position = deserialize_full_header(data, index*240 + i, expect_trailing_data=True, start_position=start_position)
            self.verify_header(header, prev_hash, target, expected_header_hash)
            prev_hash = hash_header(header)
            i = i + 1
        return bytes(stripped)"""

new = """    def verify_chunk(self, index: int, data: bytes) -> bytes:
        stripped = bytearray()
        start_position = 0
        start_height = index * 240
        prev_hash = self.get_hash(start_height - 1)
        target = self.get_target(index-1)
        i = 0
        while start_position < len(data):
            height = start_height + i
            # DigiShield: recalculate target per block after block 145000
            if height >= 145000 and i > 0:
                try:
                    target = self.get_target_digishield(height - 1)
                except Exception:
                    pass
            try:
                expected_header_hash = self.get_hash(height)
            except MissingHeader:
                expected_header_hash = None
            # Strip auxpow header for disk
            stripped.extend(data[start_position:start_position+HEADER_SIZE])
            header, start_position = deserialize_full_header(data, index*240 + i, expect_trailing_data=True, start_position=start_position)
            self.verify_header(header, prev_hash, target, expected_header_hash)
            prev_hash = hash_header(header)
            i = i + 1
        return bytes(stripped)"""

if old in content:
    content = content.replace(old, new)
    open('electrum_doge/electrum/blockchain.py', 'w', encoding='utf-8').write(content)
    print('verify_chunk patche avec succes')
else:
    print('Pattern non trouve')
