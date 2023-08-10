from datetime import timedelta

from fastapi import Depends, HTTPException, Security, status
from fastapi_jwt import JwtAccessBearer, JwtAuthorizationCredentials, JwtRefreshBearer
from sqlalchemy.orm import Session

from .config import settings
from .db import get_db
from .models.users import User
from .schemas.users import UserInResponse

access_security = JwtAccessBearer(
    secret_key=settings.SECRET_KEY,
    access_expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
)

refresh_security = JwtRefreshBearer(
    secret_key=settings.SECRET_KEY, access_expires_delta=timedelta(days=30)
)


def get_current_user(
    credentials: JwtAuthorizationCredentials = Security(access_security),
    db: Session = Depends(get_db),
):
    if not credentials:
        raise HTTPException(
            detail="Token provided is invalid",
            status_code=status.HTTP_401_UNAUTHORIZED,
        )
    return db.query(User).filter(User.id == credentials.subject["id"]).first()
