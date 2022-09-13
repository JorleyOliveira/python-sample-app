from sqlalchemy import Column, ForeignKey, Integer, String

from app.db import Base

class NominatedFilms(Base):
    __tablename__ = "nominatedfilms"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, unique=True)
    studios = Column(String(120), nullable=False)
    producers = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)

    def __repr__(self):
        return 'NominatedFilms(title=%s)' % self.title

class Winners(Base):
    __tablename__ = "winners"
    id = Column(Integer, primary_key=True, index=True)
    nominatedfilms_id = Column(Integer, ForeignKey('nominatedfilms.id'), nullable=False)

    def __repr__(self):
        return 'winners(title=%s)' % self.nominatedfilms_id
