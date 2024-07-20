import jwt

from src.user.models import VerifyTokenResponse, VerifyUser
from src.core import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def verify_token(data: VerifyUser):
    try:
        payload = jwt.decode(data.access_token, SECRET_KEY, algorithms=[ALGORITHM])
        sub: str = payload.get("sub")
        if not sub:
            return VerifyTokenResponse(success=False, message="Invalid Token")
        return VerifyTokenResponse(user_id=sub)
    except jwt.InvalidTokenError as err:
        return VerifyTokenResponse(success=False, message=str(err))
