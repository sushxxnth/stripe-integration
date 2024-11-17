from datetime import datetime, timedelta
import random
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.core.models import Response, ResponseCode
from src.core.db import get_async_session
from src.user.models import OTP, OTPRequest, OTPVerify, UserCreate, User
from datetime import timezone

from src.user.utils import create_access_token

router = APIRouter()


@router.post("/")
async def create_user(
    user: UserCreate, session: AsyncSession = Depends(get_async_session)
):
    try:
        db_user = User(**user.model_dump())
        db_user.is_parent = True
        session.add(db_user)
        await session.commit()
        await session.refresh(db_user)
        # Add age to response
        response = db_user.model_dump()
        response["age"] = db_user.age()
        return Response(
            response_code=ResponseCode.success,
            message="User Created Successfully",
            data=response,
        )
    except Exception as err:
        print(err)
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Internal Server Error"
        )


def generate_otp():
    return "".join([str(random.randint(0, 9)) for _ in range(6)])


@router.post("/otp/request")
async def request_otp(
    otp_request: OTPRequest, session: AsyncSession = Depends(get_async_session)
):
    objs = await session.exec(select(User).where(User.mobile == otp_request.mobile))
    user = objs.first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    otp_code = generate_otp()
    expires_at = datetime.now() + timedelta(minutes=5)

    db_otp = OTP(mobile=otp_request.mobile, otp_code=otp_code, expires_at=expires_at)
    session.add(db_otp)
    await session.commit()

    # send_otp_sms(otp_request.mobile, otp_code)
    return Response(
        response_code=ResponseCode.success,
        message="OTP sent successfully",
        data={"otp": otp_code},
    )


@router.post("/otp/verify")
async def verify_otp(
    otp_verify: OTPVerify, session: AsyncSession = Depends(get_async_session)
):
    statement = select(OTP).where(
        OTP.mobile == otp_verify.mobile,
        OTP.otp_code == otp_verify.otp,
        OTP.expires_at > datetime.now(),
        OTP.is_verified == False,
    )
    objs = await session.exec(statement)
    otp = objs.scalars().first()
    if not otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    otp.is_verified = True

    user = await session.exec(select(User).where(User.mobile == otp_verify.mobile))
    user = user.scalars().first()

    await session.commit()

    access_token = create_access_token({"sub": str(user.id)})
    return Response(
        response_code=ResponseCode.success,
        message="OTP verified successfully",
        data={"access_token": access_token, "type": "bearer"},
    )
