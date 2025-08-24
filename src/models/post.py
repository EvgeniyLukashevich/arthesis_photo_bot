from sqlalchemy import Boolean, Column, Integer, String, Text, DateTime
from src.database import Base


class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    photo_path = Column(String, nullable=False)  # путь к файлу
    title = Column(String, nullable=True)
    author = Column(String, nullable=True)
    date = Column(String, nullable=True)  # строка ISO
    location = Column(String, nullable=True)
    caption = Column(Text, nullable=True)
    header = Column(String, nullable=True)  # новое поле
    tags = Column(String, nullable=True)  # строка JSON-массива
    is_active = Column(Boolean, default=True, nullable=False)
    shown = Column(Boolean, default=False, nullable=False)
