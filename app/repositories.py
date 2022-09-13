
from sqlalchemy.orm import Session

from . import models, schemas

class NominatedFilmsRepo:

    async def create(db: Session, nominatedFilms: schemas.NominatedFilmsCreate):
            db_nominatedFilms = models.NominatedFilms(name=nominatedFilms.name)
            db.add(db_nominatedFilms)
            db.commit()
            db.refresh(db_nominatedFilms)
            return db_nominatedFilms

    def fetch_by_id(db: Session,_id:int):
        return db.query(models.NominatedFilms).filter(models.NominatedFilms.id == _id).first()

    def fetch_by_name(db: Session,name:str):
        return db.query(models.NominatedFilms).filter(models.NominatedFilms.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.NominatedFilms).offset(skip).limit(limit).all()

    async def delete(db: Session,_id:int):
        db_nominatedFilms= db.query(models.NominatedFilms).filter_by(id=_id).first()
        db.delete(db_nominatedFilms)
        db.commit()

    async def update(db: Session,nominatedFilms_data):
        db.merge(nominatedFilms_data)
        db.commit()

class WinnersRepo:

    async def create(db: Session, winners: schemas.WinnersCreate):
            db_winners = models.Winners(name=winners.name)
            db.add(db_winners)
            db.commit()
            db.refresh(db_winners)
            return db_winners

    def fetch_by_id(db: Session,_id:int):
        return db.query(models.Winners).filter(models.Winners.id == _id).first()

    def fetch_by_name(db: Session,name:str):
        return db.query(models.Winners).filter(models.Winners.name == name).first()

    def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Winners).offset(skip).limit(limit).all()

    async def delete(db: Session,_id:int):
        db_winners= db.query(models.Winners).filter_by(id=_id).first()
        db.delete(db_winners)
        db.commit()

    async def update(db: Session,winners_data):
        db.merge(winners_data)
        db.commit()