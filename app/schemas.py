from pydantic import BaseModel

class NominatedFilmsBase(BaseModel):
    title: str
    studios: str
    year: int

class ProducersBase(BaseModel):
    name: str

class FilmsProducersBase(BaseModel):
    nominatedfilms_id: int
    producers_id: int

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

class Producers(ProducersBase):
    id: int

    class Config:
        orm_mode = True

class FilmsProducers(FilmsProducersBase):
    id: int

    class Config:
        orm_mode = True

class ProducersCreate(ProducersBase):
    pass

class FilmsProducersCreate(FilmsProducersBase):
    pass