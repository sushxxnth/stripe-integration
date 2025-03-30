from datetime import datetime, timedelta
import jwt

from src.core import settings
from datetime import timezone

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


# def verify_token(data: VerifyUser):
#     try:
#         payload = jwt.decode(data.access_token, SECRET_KEY, algorithms=[ALGORITHM])
#         sub: str = payload.get("sub")
#         if not sub:
#             return VerifyTokenResponse(success=False, message="Invalid Token")
#         return VerifyTokenResponse(user_id=sub)
#     except jwt.InvalidTokenError as err:
#         return VerifyTokenResponse(success=False, message=str(err))


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
