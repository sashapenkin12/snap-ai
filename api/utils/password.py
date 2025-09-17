from passlib.context import CryptContext

pwd_context = CryptContext(schemes=['argon2'], deprecated='auto')


def verify_password(plain_password: str, hashed_password) -> bool:
    return pwd_context.verify(
        secret=plain_password,
        hash=hashed_password,
    )


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)
