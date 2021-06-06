"""
Author: Rendani Gangazhe

General digital signature functions.
"""
from typing import Tuple
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes, serialization


def decrypt_ciphertext(private_key: rsa.RSAPrivateKeyWithSerialization, ciphertext: bytes) -> bytes:
    """
    Decrypt `ciphertext` represented as bytes using `private_key`.
    """
    return private_key.decrypt(
        ciphertext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def encrypt_plaintext(public_key: rsa.RSAPublicKeyWithSerialization, plaintext: bytes) -> bytes:
    """
    Encrypt `plaintext` respented as bytes using `public_key`.
    """
    return public_key.encrypt(
        plaintext,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )


def verify_signature(doc: bytes, signature: bytes, public_key: rsa.RSAPublicKeyWithSerialization) -> bool:
    """
    Check wether a document is valid.

    Args:
        doc         - the signed document to be verified
        signature   - the signature with which the document was signed
        public_key  - the public key
    """
    try:
        public_key.verify(signature=signature, data=doc,
                          padding=padding.PSS(
                              mgf=padding.MGF1(hashes.SHA256()),
                              salt_length=padding.PSS.MAX_LENGTH
                          ),
                          algorithm=hashes.SHA256()
                          )
        return True
    except:
        pass

    return False


def generate_key_pair() -> Tuple[rsa.RSAPrivateKeyWithSerialization, rsa.RSAPublicKeyWithSerialization]:
    """Generate a new RSA key pair"""
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
        backend=default_backend())

    publick_key = private_key.public_key()

    return (private_key, publick_key)


def sign_with_private_key(message: bytes, private_key: rsa.RSAPrivateKeyWithSerialization) -> bytes:
    """
    Signs a massage with a private_key

    Args:
        message     - the message to be signed
        private_key - the key to sing the message with

    Returns:
        The corresponding signature after signing the message

    >>> keys = generate_key_pair()
    >>> private_key, public_key = keys[0], keys[1]
    >>> message = b'This is the way'
    >>> signature = sign_with_private_key(message, private_key)
    >>> verify_signature(message, signature, public_key) is True
    True
    """
    return private_key.sign(data=message,
                            padding=padding.PSS(
                                mgf=padding.MGF1(hashes.SHA256()),
                                salt_length=padding.PSS.MAX_LENGTH
                            ),
                            algorithm=hashes.SHA256())


def serialize_public_key(key_data: bytes):
    """Serialize a public key given raw `key_data`."""
    return serialization.load_pem_public_key(key_data, backend=default_backend())


def serialize_private_key(key_data: bytes):
    """Serialize a private key given raw `key_data`."""
    return serialization.load_pem_private_key(data=key_data, password=None, backend=default_backend())


def read_file_from_disk(file_name: str) -> bytes:
    """Read a file from disk."""
    with open(file_name, 'rb') as file:
        data = file.read()
    return data


def save_public_key_to_disk(key: rsa.RSAPublicKeyWithSerialization):
    """Save a public key to disk and encode is using PEM encoding."""
    with open('new_public_key', 'xb') as new_file:
        new_file.write(
            key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            )
        )


def save_bytestring_to_disk(data: bytes, file_name='new_file'):
    """Save a bytestring to a new file called `file_name`."""
    with open(file_name, 'xb') as new_file:
        new_file.write(data)
