import random
import string


def random_string_digits(length=6):
    letters_and_digits = string.ascii_letters + string.digits
    return ''.join(random.choice(letters_and_digits) for _ in range(length))


def random_string(length=10):
    return ''.join(random.choice(string.ascii_letters) for _ in range(length))
