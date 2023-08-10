from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..db import get_db
from ..models.users import User
from ..schemas.users import UserInDB, UserInResponse
from ..utils import hash

user_router = APIRouter(prefix="/users", tags=["Users"])


@user_router.post("/", response_model=UserInResponse)
async def create_user(user: UserInDB, db: Session = Depends(get_db)):
    # hash password
    user.password = hash(password=user.password)
    new_user = User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@user_router.get("/", response_model=UserInResponse)
async def get_user(id: str, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id {id} does not exist",
        )
    return user
