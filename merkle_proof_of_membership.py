import hashlib


def check_proof(top_hash, data_hash, proofs: list) -> bool:
    """
    Checks whether a given proof of membership in a Merkle tree is valid.

    inputs:
      top_hash - The top hash of the Merkle tree t.

      data_hash - The hash of the data item x that is supposed to be in the tree.

      proof - The proof in the form of a list of pairs containing a data hash and.
              a string "Left" or "Right" to encode the direction.

    outputs:
      A boolean indicating


    test:
    Test your function with this input:

    >>> top_hash = '56e962de2b5cdc0b8cd8d1929abfa96c831f64e0cf5ad23420ece8cb2ae77ddc'
    >>> data_hash = '3e744b9dc39389baf0c5a0660589b8402f3dbb49b89b3e75f2c9355852a3c677'
    >>> proof = [('9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0', "Left"), ('7d9bf113ceed7a50bacb7361ba2ac0f52f0a23f4d0357a6d69ba4d23cb0afb4a', "Right")]
    >>> check_proof(top_hash, data_hash, proof) == True
    True

    >>> top_hash = '56e962de2b5cdc0b8cd8d1929abfa96c831f64e0cf5ad23420ece8cb2ae77ddc'
    >>> data_hash = 'superfake'
    >>> proof = [('9834876dcfb05cb167a5c24953eba58c4ac89b1adf57f28f2f9d09af107ee8f0', "Left"), ('7d9bf113ceed7a50bacb7361ba2ac0f52f0a23f4d0357a6d69ba4d23cb0afb4a', "Right")]
    >>> check_proof(top_hash, data_hash, proof) == False
    True
    """
    assert proofs, 'Proof list cannot be empty'
    next_hash = data_hash

    def hash(data): return hashlib.sha256(
        bytearray(data, 'utf-8')).hexdigest()

    for proof in proofs:
        if 'Left' in proof:
            combined_hash = proof[0] + next_hash
            next_hash = hash(combined_hash)
        else:
            combined_hash = next_hash + proof[0]
            next_hash = hash(combined_hash)

    return top_hash == next_hash
