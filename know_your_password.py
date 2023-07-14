import random
import string

import bcrypt

salt = bcrypt.gensalt(rounds=12)
hashed_login_password = bcrypt.hashpw("admin".encode("utf-8"), salt)
print("hashed_login_password=", hashed_login_password)
print("decode_hashed_login_password=", hashed_login_password.decode("utf-8"))
login_secretkey = ''.join((random.choice(string.ascii_letters + string.digits)) for x in range(32))
print("login_secretkey=", login_secretkey)

user_str_password = "fILuGWdX"
user_byte_password = user_str_password.encode("utf-8")
db_str_password = "$2b$12$ALWMpaNcBduXh7W8BLv/4.grVdF1f2rljUqINeyP5Y2IzNLAM/O2u"
db_byte_password = db_str_password.encode("utf-8")
print(bcrypt.checkpw(user_byte_password, db_byte_password))