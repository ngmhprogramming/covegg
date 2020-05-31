from hashlib import sha256

salt = "verygoodproject"

def hash(password):
    password += salt
    return sha256(password.encode("utf-8")).hexdigest()