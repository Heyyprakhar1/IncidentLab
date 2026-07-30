"""
Password hashing utilities.

Purpose
-------
Provide password hashing and verification helpers.

Responsibilities
----------------
- Hash plaintext passwords.
- Verify plaintext passwords against stored hashes.

Non-Responsibilities
--------------------
- User authentication.
- JWT generation.
- Database operations.
"""

from pwdlib import PasswordHash

password_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    """
    Hash a plaintext password.
    """
    return password_hash.hash(password)


def verify_password(
    plain_password: str,
    hashed_password: str,
) -> bool:
    """
    Verify a plaintext password against its hash.
    """
    return password_hash.verify(
        plain_password,
        hashed_password,
    )
