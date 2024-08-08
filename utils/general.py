import bcrypt

def get_hashed_pass(password):
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

def check_passwords(password, stored_password):
    return bcrypt.checkpw(password.encode('utf-8'), stored_password)