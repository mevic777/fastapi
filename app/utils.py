from passlib.context import CryptContext

# we use pwd_context to hash our password so even if
# hackers have our password, they cannot unhash it
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash(password: str):
    return pwd_context.hash(password)


def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
