from sqlalchemy import Boolean, Column, Integer, String, Text, JSON
from src.database import Base


class AdPost(Base):
    __tablename__ = "ad_posts"
    id = Column(Integer, primary_key=True)
    photo_path = Column(String, nullable=False, default='/photos/0000_ad_default.jpg')
    erid = Column(String, nullable=True)
    advertiser_name = Column(String, nullable=True)
    advertiser_link = Column(String, nullable=True)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=True)
    link = Column(String, nullable=True)
    tags = Column(String, nullable=True)
    schedule = Column(JSON, nullable=False)    # даты
    is_active = Column(Boolean, default=True, nullable=False)
