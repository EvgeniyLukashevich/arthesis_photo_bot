from sqlalchemy import Boolean, Column, Integer, String, Text, JSON
from src.database import Base


class InstantPost(Base):
    __tablename__ = "instant_posts"
    id = Column(Integer, primary_key=True)
    photo_path = Column(String, nullable=False, default='/photos/0000_instant_default.jpg')
    text = Column(Text, nullable=True)
    tags = Column(String, nullable=True)
    schedule = Column(JSON, nullable=False)    # даты
    is_active = Column(Boolean, default=True, nullable=False)
