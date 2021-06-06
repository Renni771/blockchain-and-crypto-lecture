import hashlib


class Block:
    def __init__(self, data: bytearray, prev=None):
        self.data = data
        self.prev = prev
        self.prev_hash = prev.digest() if prev is not None else bytearray(256)

    def digest(self):
        m = hashlib.sha256()
        m.update(self.prev_hash)
        m.update(self.data)
        return bytearray(m.hexdigest(), 'utf-8')

    def verify(self, root_hash):
        if (self.digest() != root_hash):
            print('Couldn\'t verify hash for the block containing {}.'.format(
                self.data))
            return False

        if self.prev is None:
            return True

        return self.prev.verify(self.prev_hash)


class Blockchain:
    def __init__(self):
        self.root_hash = bytearray(256)
        self.list = None

    def add_block(self, data: bytearray):
        new_block = Block(data, self.list)
        self.root_hash = new_block.digest()
        self.list = new_block

    def verify(self):
        return not self.list or self.list.verify(self.root_hash)

    def __str__(self):
        head = self.list
        bc = '[TAIL] '
        while head is not None:
            bc += head.data.decode() + ' -> '
            head = head.prev
        bc += ' [HEAD]'

        return bc
