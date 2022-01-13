from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import text
from sqlalchemy.sql.sqltypes import TIMESTAMP

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, nullable=False, unique=True, index=True)
    password = Column(String, nullable=False)
    is_active = Column(Boolean, nullable=False, server_default="TRUE")
    is_superuser = Column(Boolean, nullable=False, server_default="FALSE")
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))


# class Customer(Base):
#     __tablename__ = "customers"
#
#     id = Column(Integer, primary_key=True, index=True)
#     first_name = Column(String, nullable=False)
#     last_name = Column(String, nullable=True)
#     creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
#     created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text('now()'))
#
#     creator = relationship("User")