from sqlalchemy import Column, String, DateTime, Integer

from extensions import Model
from utils.helper import Timestamp


class Videos(Model, Timestamp):
    id = Column(Integer, primary_key=True, autoincrement=True)
    video_id = Column(Integer, unique=True)
    title = Column(String(32), index=True, nullable=False)
    description = Column(String(256), nullable=True)
    publish_date_timestamp = Column(DateTime, nullable=False, index=True)
    thumbnail_url = Column(String(64), nullable=False)
