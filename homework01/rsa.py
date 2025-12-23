"""RSA encryption and decryption implementation."""

import random
from typing import List, Tuple


def is_prime(n: int) -> bool:
    """
    >>> is_prime(2)
    True
    >>> is_prime(11)
    True
    >>> is_prime(8)
    False
    """
    if n < 2:
        return False
    if n == 2 or n % 2 == 0:
        return n == 2

    # Проверяем делители от 3 до sqrt(n)
    i = 3
    while i * i <= n:
        if n % i == 0:
            return False
        i += 2
    return True


def gcd(a: int, b: int) -> int:
    """
    >>> gcd(12, 15)
    3
    >>> gcd(3, 7)
    1
    """
    while b != 0:
        a, b = b, a % b
    return a


def multiplicative_inverse(e: int, phi: int) -> int:
    """
    >>> multiplicative_inverse(7, 40)
    23
    """
    # Находим x такое, что (e * x) % phi = 1
    a, b, u = 0, phi, 1
    while e > 0:
        quotient = b // e
        r = b % e
        m = a - u * quotient
        b, e, a, u = e, r, u, m
    if b == 1:
        return a % phi
    raise ValueError("Multiplicative inverse does not exist")


def generate_keypair(p: int, q: int) -> Tuple[Tuple[int, int], Tuple[int, int]]:
    """
    Generate RSA public and private keypair.

    Args:
        p: First prime number
        q: Second prime number

    Returns:
        Tuple containing public key (e, n) and private key (d, n)
    """
    if not (is_prime(p) and is_prime(q)):
        raise ValueError("Both numbers must be prime.")
    if p == q:
        raise ValueError("p and q cannot be equal")

    # n = pq
    n = p * q

    # phi = (p-1)(q-1)
    phi = (p - 1) * (q - 1)

    # Choose an integer e such that e and phi(n) are coprime
    e = random.randrange(1, phi)

    # Use Euclid's Algorithm to verify that e and phi(n) are comprime
    g = gcd(e, phi)
    while g != 1:
        e = random.randrange(1, phi)
        g = gcd(e, phi)

    # Use Extended Euclid's Algorithm to generate the private key
    d = multiplicative_inverse(e, phi)
    # Return public and private keypair
    # Public key is (e, n) and private key is (d, n)
    return ((e, n), (d, n))


def encrypt(pk: Tuple[int, int], plaintext: str) -> List[int]:
    """
    Encrypt plaintext using RSA public key.

    Args:
        pk: Public key tuple (e, n)
        plaintext: Message to encrypt

    Returns:
        List of encrypted integers
    """
    # Unpack the key into it's components
    key, n = pk
    # Convert each letter in the plaintext to numbers based on
    # the character using a^b mod m
    cipher = [(ord(char) ** key) % n for char in plaintext]
    # Return the array of bytes
    return cipher


def decrypt(pk: Tuple[int, int], ciphertext: List[int]) -> str:
    """
    Decrypt ciphertext using RSA private key.

    Args:
        pk: Private key tuple (d, n)
        ciphertext: List of encrypted integers

    Returns:
        Decrypted plaintext string
    """
    # Unpack the key into its components
    key, n = pk
    # Generate the plaintext based on the ciphertext and key using a^b mod m
    plain = [chr((char**key) % n) for char in ciphertext]
    # Return the array of bytes as a string
    return "".join(plain)


if __name__ == "__main__":
    print("RSA Encrypter/ Decrypter")
    prime_p = int(input("Enter a prime number (17, 19, 23, etc): "))
    prime_q = int(input("Enter another prime number (Not one you entered above): "))
    print("Generating your public/private keypairs now . . .")
    public, private = generate_keypair(prime_p, prime_q)
    print("Your public key is ", public, " and your private key is ", private)
    message = input("Enter a message to encrypt with your private key: ")
    encrypted_msg = encrypt(private, message)
    print("Your encrypted message is: ")
    print("".join(map(str, encrypted_msg)))
    print("Decrypting message with public key ", public, " . . .")
    print("Your message is:")
    print(decrypt(public, encrypted_msg))
