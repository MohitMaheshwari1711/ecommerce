import hashlib
from django.utils.crypto import get_random_string



def generate_activation_key(email):
    chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
    secret_key = get_random_string(20, chars)
    return str(hashlib.sha256((secret_key + email).encode('utf-8')).hexdigest())