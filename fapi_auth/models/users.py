from sqlalchemy import TIMESTAMP, Boolean, Column, Integer, String
from sqlalchemy.sql import func
from sqlalchemy.sql.expression import text

from ..db import Base


class DateMixins(object):
    created_at = Column(TIMESTAMP(timezone=True), server_default=text("now()"))
    updated_at = Column(
        TIMESTAMP(timezone=True), server_default=text("now()"), onupdate=func.now()
    )


class User(Base, DateMixins):
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String, nullable=False, unique=True)
    name = Column(String, nullable=False)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, default=True, server_default=text("true"))
