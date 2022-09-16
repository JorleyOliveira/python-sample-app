from sqlalchemy import Column, ForeignKey, Integer, String

from app.db import Base

class Producers(Base):
    __tablename__ = "producers"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False, unique=True)

    def __repr__(self):
        return 'Producers(name=%s)' % self.name

class NominatedFilms(Base):
    __tablename__ = "nominatedfilms"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(120), nullable=False, unique=True)
    studios = Column(String(120), nullable=False)
    year = Column(Integer, nullable=False)

    def __repr__(self):
        return 'NominatedFilms(title=%s)' % self.title

class Winners(Base):
    __tablename__ = "winners"
    id = Column(Integer, primary_key=True, index=True)
    nominatedfilms_id = Column(Integer, ForeignKey('nominatedfilms.id'), nullable=False)

    def __repr__(self):
        return 'winners(title=%s)' % self.nominatedfilms_id

class FilmsProducers(Base):
    __tablename__ = "filmsproducers"
    id = Column(Integer, primary_key=True, index=True)
    nominatedfilms_id = Column(Integer, ForeignKey('nominatedfilms.id'), nullable=False)
    producers_id = Column(Integer, ForeignKey('producers.id'), nullable=False)

    def __repr__(self):
        return 'filmsproducers(nominatedfilms_id=%s)' % self.nominatedfilms_id
