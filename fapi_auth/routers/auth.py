from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from ..db import get_db
from ..models.users import User
from ..oauth2 import access_security, get_current_user, refresh_tokens, refresh_security
from ..schemas.users import Token, UserInResponse
from ..utils import verify

auth_router = APIRouter(prefix="/auth", tags=["Auth"])


@auth_router.post("/login", response_model=Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid credentials"
        )
    if not verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="Invalid Credentials"
        )
    # create token
    payload_data = {"id": user.id}
    access_token = access_security.create_access_token(subject=payload_data)
    refresh_token = refresh_security.create_refresh_token(subject=payload_data)
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "refresh_token": refresh_token,
    }


@auth_router.get("/current", response_model=UserInResponse)
def get_curr_user(current_user = Depends(get_current_user)):
    return current_user


@auth_router.post("/refresh")
def refresh(
        tokens: dict = Depends(refresh_tokens)
):
    return tokens