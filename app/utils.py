from pwdlib import PasswordHash

# Password hashing context for securely storing passwords
password_hash_context = PasswordHash.recommended()

def hash_password(plain_password: str) -> str:
    """Hash a plain password."""
    return password_hash_context.hash(plain_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify a plain password against a hashed password."""
    return password_hash_context.verify(plain_password, hashed_password)