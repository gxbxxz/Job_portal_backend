from passlib.context import CryptContext

pwd_cxt=CryptContext(schemes=["bcrypt"])

class Hash():
    def brycpt(password:str):
        return pwd_cxt.hash(password)
    
    def verify(plain_password,hash_password):
        return pwd_cxt.verify(plain_password,hash_password)
    