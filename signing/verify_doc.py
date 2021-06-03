"""
Author: Rendani Gangazhe
"""
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes


def verify_doc(doc: bytes, signature: bytes, public_key: rsa.RSAPublicKeyWithSerialization) -> bool:
    """
    Check wether a document is valid.

    Args:
        doc         - the signed document to be verified
        signature   - the signature with which the document was signed
        public_key  - the public key

    >>> f = open('public_key', 'rb')
    >>> public_key = serialization.load_pem_public_key(f.read(), default_backend())
    >>> f = open('document.txt', 'rb')
    >>> document = f.read()
    >>> f = open('signature', 'rb')
    >>> signature = f.read()
    >>> verify_doc(document, signature, public_key) == True
    True

    """
    try:
        verify = public_key.verify(signature=signature, data=doc,
                                   padding=padding.PSS(
                                       mgf=padding.MGF1(hashes.SHA256()),
                                       salt_length=padding.PSS.MAX_LENGTH
                                   ),
                                   algorithm=hashes.SHA256()
                                   )
    except:
        pass

    return True if verify is None else False
