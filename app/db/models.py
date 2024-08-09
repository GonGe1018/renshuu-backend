from sqlalchemy import Column, Integer, String, Text, DateTime

from app.db.database import Base


class Users(Base):
    __tablename__ = "uesrs"

    cuid = Column(String, primary_key=True, nullable=False)
    user_name = Column(String, nullable=False)
    email = Column(String, nullable=False)
    password = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
    discription = Column(Text, nullable=True)