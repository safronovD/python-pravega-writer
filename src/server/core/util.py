import random
import string


def id_generator(size=10, chars=string.ascii_letters + string.digits):
    """Generate random id."""
    return ''.join(random.choice(chars) for _ in range(size))
