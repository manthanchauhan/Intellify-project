from passlib.context import CryptContext


def encrypt_password(password) -> str:
    """
    Hashes the password
    :param password: password provided by user, as str.
    :return: Hash of the password, str.
    """
    # define a context for hashing
    # we can later hide this in some .env file
    context = CryptContext(schemes=['pbkdf2_sha256'],
                           default='pbkdf2_sha256',
                           pbkdf2_sha256__default_rounds=30000,
                           )
    return context.encrypt(password)


def check_password(user_provided, encrypted) -> bool:
    """
    Checks if user provided password & encrypted hash correspond to same password.
    :param user_provided: password provided by user during login.
    :param encrypted: password hash stored in db during signup.
    :return: True/False
    """
    context = CryptContext(schemes=['pbkdf2_sha256'],
                           default='pbkdf2_sha256',
                           pbkdf2_sha256__default_rounds=30000,
                           )
    return context.verify(user_provided, encrypted)