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


def refresh_tokens(credentials: JwtAuthorizationCredentials = Security(refresh_security)
):
    # Update access/refresh tokens pair
    # We can customize expires_delta when creating
    access_token = access_security.create_access_token(subject=credentials.subject)
    refresh_token = refresh_security.create_refresh_token(subject=credentials.subject, expires_delta=timedelta(days=30))

    return {"access_token": access_token, "token_type": "bearer", "refresh_token": refresh_token}