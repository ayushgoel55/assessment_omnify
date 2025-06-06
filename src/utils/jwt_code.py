#
# from datetime import datetime, timedelta
#
# import jwt
#
#
# SECRET_KEY = "ASSESSMENT@123"
# ALGORITHM = "HS256"
# ACCESS_TOKEN_EXPIRE_MINUTES = 30
#
# def create_access_token(data: dict, expires_delta: timedelta = None):
#     to_encode = data.copy()
#     expire = datetime.now() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
#     to_encode.update({"exp": expire})
#     return jwt.encode(payload=to_encode,key= SECRET_KEY, algorithm=ALGORITHM)
#
#
# def decode_token(token: str):
#     try:
#         payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
#         return payload
#     except jwt.PyJWTError:
#         return None