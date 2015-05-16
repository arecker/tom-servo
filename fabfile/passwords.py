import random
import string


def get_secret_key():
    """
    Generates a new Django secret key
    """
    return get_password(length=100)


def get_password(length=10):
    """
    Generates a new password
    """
    return ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(length))

