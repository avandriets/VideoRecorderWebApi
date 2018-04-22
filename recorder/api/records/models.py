import datetime
from sqlalchemy import Column, ForeignKey, Integer, String, Text, Boolean
from sqlalchemy import DateTime
from sqlalchemy.orm import relationship
from recorder.database import db


class RecordsSet(db.Model):
    __tablename__ = 'RecordsSet'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    recordings = relationship('VideoCollectionItem')
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'collectionName': self.name,
            'recordings': [c.serialize for c in self.recordings],
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }


class VideoCollectionItem(db.Model):
    __tablename__ = 'VideoCollectionItem'

    id = Column(Integer, primary_key=True)
    records_set_id = Column(ForeignKey('RecordsSet.id'))
    records_set = relationship('RecordsSet')
    video_id = Column(ForeignKey('Video.id'))
    video = relationship('Video')
    start_time = Column(Integer, nullable=False)
    finish_time = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow)

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'records_set_id': self.records_set_id,
            'startTime': self.start_time,
            'finishTime': self.finish_time,
            'video': self.video.serialize,
            'createdAt': self.created_at,
            'updatedAt': self.updated_at
        }


class Video(db.Model):
    __tablename__ = 'Video'

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    url = Column(String(255), nullable=False)

    def get_id(self):
        return self.id

    @property
    def serialize(self):
        """Return object data in easily serializeable format"""
        return {
            'id': self.id,
            'name': self.name,
            'url': self.url
        }
