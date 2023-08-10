from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(secret=password)


def verify(password: str, hashed_password: str):
    return pwd_context.verify(secret=password, hash=hashed_password)
