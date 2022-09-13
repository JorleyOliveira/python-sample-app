from pydantic import BaseModel

class NominatedFilmsBase(BaseModel):
    title: str
    studios: str
    producers: str
    year: int

class WinnersBase(BaseModel):
    nominatedfilms_id: int

class NominatedFilmsCreate(NominatedFilmsBase):
    pass

class WinnersCreate(WinnersBase):
    pass

class NominatedFilms(NominatedFilmsBase):
    id: int

    class Config:
        orm_mode = True

class Winners(WinnersBase):
    id: int

    class Config:
        orm_mode = True