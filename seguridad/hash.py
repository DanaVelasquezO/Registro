import bcrypt

def hash_clave(clave):
    return bcrypt.hashpw(clave.encode("utf-8"), bcrypt.gensalt())

def verificar_clave(clave, hashed):
    return bcrypt.checkpw(clave.encode("utf-8"), hashed.encode("utf-8"))