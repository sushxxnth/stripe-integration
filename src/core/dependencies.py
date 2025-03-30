from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from redis import Redis, asyncio as aioredis
from src.core.utils import convert_data_to_dict
from src.core import settings
from src.user.models import User, VerifyUser
from src.user.utils import verify_token

security = HTTPBearer()


async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
) -> User:
    token = verify_token(VerifyUser(access_token=credentials.credentials))
    if not token.success:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail=token.message
        )
