import hashlib
import time

def get_current_epoch():
    return int(time.time())

def hash(string):
    return hashlib.sha256(string.encode()).hexdigest()

def check_logged_in(user):
    if user.is_authenticated:
        return True
    return False


