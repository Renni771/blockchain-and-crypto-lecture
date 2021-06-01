def direct_neighbors(p1: list, p2: list) -> bool:
    """
    Checks whether two proofs of membership in a Merkle tree refer to direct neighbors in the tree.

    Args:
        p1 - The first p
        p2 - The second p

    >>> p1 = [('Hash 0-0', 'Left'), ('Hash 1', 'Right')]
    >>> p2 = [('Hash 1-1', 'Right'), ('Hash 0', 'Left')] 
    >>> direct_neighbors(p1, p2) == True
    True
    """
    assert p1 and p2, 'The proofs may not be empty.'

    def leftmost(proofs: list): return all(x[1] == 'Right' for x in proofs)
    def rightmost(proofs: list): return all(x[1] == 'Left' for x in proofs)

    if p1[-1][0] == p2[-1][0] and p1[-1][1] == p2[-1][1]:
        direct_neighbors(p1[:-1], p2[:-1])

    if p1[-1][1] == 'Left' and p2[-1][1] == 'Right':
        return leftmost(p1[:-1]) and rightmost(p2[:-1])

    if p1[-1][1] == 'Right' and p2[-1][1] == 'Left':
        return rightmost(p1[:-1]) and leftmost(p2[:-1])
