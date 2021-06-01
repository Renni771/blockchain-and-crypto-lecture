import hashlib


class Leaf:
    def __init__(self, data):
        self.hash = hashlib.sha256(bytearray(data, 'utf-8')).hexdigest()


class Node:
    def __init__(self, left=None, right=None):
        self.left = left
        self.right = right
        self.hash = self.digest()

    def digest(self) -> str:
        m = hashlib.sha256()
        m.update(bytearray(self.left.hash + self.right.hash, 'utf-8'))
        return m.hexdigest()


class MerkleTree:
    def __init__(self, data: list):
        assert len(data) != 0
        nodes = list(map(Leaf, data))

        while len(nodes) != 1:
            newNodes = []
            for i in range(0, len(nodes) - 1, 2):
                newNodes.append(Node(nodes[i], nodes[i+1]))

            if len(nodes) % 2 == 1:
                newNodes.append(nodes[-1])

            nodes = newNodes

        self.tree = nodes[0]
        self.rootHash = self.tree.hash
