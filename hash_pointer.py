import hashlib

class HashPointer():
    def __init__(self, target: bytearray):
        self.target = target
        self.hash = self.digest()

    def verify(self):
        return self.hash == self.digest()

    def digest(self):
        m = hashlib.sha256(self.target)
        return m.hexdigest()

    
