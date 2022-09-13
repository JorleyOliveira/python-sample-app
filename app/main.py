from typing import List, Optional

import uvicorn
from fastapi import Depends, FastAPI, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
import time

import app.models as models
import app.schemas as schemas
from app.db import get_db, engine
from app.repositories import NominatedFilmsRepo, WinnersRepo
from app.utils import load_movies, count_producers_by_interval

app = FastAPI(title="Application",
              description="Example FastAPI Application with Swagger and Sqlalchemy",
              version="1.0.0", )

@app.on_event("startup")
async def startup_event():
    models.Base.metadata.drop_all(bind=engine)
    models.Base.metadata.create_all(bind=engine)
    nominated_films_qtd, winners_qtd = load_movies()
    print(f"nominated_films = {nominated_films_qtd}")
    print(f"winners = {winners_qtd}")

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})


@app.middleware("http")
async def add_process_time_header(request, call_next):
    print('inside middleware!')
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(f'{process_time:0.4f} sec')
    return response

@app.post('/nominatedfilms', tags=["Nominatedfilms"], response_model=schemas.NominatedFilms, status_code=201)
async def create_nominatedfilms(nominatedfilms_request: schemas.NominatedFilmsCreate, db: Session = Depends(get_db)):
    """
    Create a Nominatedfilms and save it in the database
    """
    db_nominatedfilms = NominatedFilmsRepo.fetch_by_name(db, name=nominatedfilms_request.name)
    print(db_nominatedfilms)
    if db_nominatedfilms:
        raise HTTPException(status_code=400, detail="Nominatedfilms already exists!")

    return await NominatedFilmsRepo.create(db=db, nominatedfilms=nominatedfilms_request)


@app.get('/nominatedfilms', tags=["Nominatedfilms"], response_model=List[schemas.NominatedFilms])
def get_all_nominatedfilms(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Nominatedfilms stored in database
    """
    if name:
        nominatedfilms = []
        db_nominatedfilms = NominatedFilmsRepo.fetch_by_name(db, name)
        print(db_nominatedfilms)
        nominatedfilms.append(db_nominatedfilms)
        return nominatedfilms
    else:
        return NominatedFilmsRepo.fetch_all(db)


@app.get('/nominatedfilms/{nominatedfilms_id}', tags=["Nominatedfilms"], response_model=schemas.NominatedFilms)
def get_nominatedfilms(nominatedfilms_id: int, db: Session = Depends(get_db)):
    """
    Get the Nominatedfilms with the given ID provided by User stored in database
    """
    db_nominatedfilms = NominatedFilmsRepo.fetch_by_id(db, nominatedfilms_id)
    if db_nominatedfilms is None:
        raise HTTPException(status_code=404, detail="Nominatedfilms not found with the given ID")
    return db_nominatedfilms


@app.delete('/nominatedfilms/{nominatedfilms_id}', tags=["Nominatedfilms"])
async def delete_nominatedfilms(nominatedfilms_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_nominatedfilms = NominatedFilmsRepo.fetch_by_id(db, nominatedfilms_id)
    if db_nominatedfilms is None:
        raise HTTPException(status_code=404, detail="Nominatedfilms not found with the given ID")
    await NominatedFilmsRepo.delete(db, nominatedfilms_id)
    return "Nominatedfilms deleted successfully!"

@app.post('/winners', tags=["Winners"], response_model=schemas.Winners, status_code=201)
async def create_winners(winners_request: schemas.WinnersCreate, db: Session = Depends(get_db)):
    """
    Create a Winners and save it in the database
    """
    db_winners = WinnersRepo.fetch_by_name(db, name=winners_request.name)
    print(db_winners)
    if db_winners:
        raise HTTPException(status_code=400, detail="Winners already exists!")

    return await WinnersRepo.create(db=db, winners=winners_request)


@app.get('/winners', tags=["Winners"], response_model=List[schemas.Winners])
def get_all_winners(name: Optional[str] = None, db: Session = Depends(get_db)):
    """
    Get all the Winners stored in database
    """
    if name:
        winners = []
        db_winners = WinnersRepo.fetch_by_name(db, name)
        print(db_winners)
        winners.append(db_winners)
        return winners
    else:
        return WinnersRepo.fetch_all(db)


@app.get('/winners/{winner_id}', tags=["Winners"], response_model=schemas.Winners)
def get_winners(winner_id: int, db: Session = Depends(get_db)):
    """
    Get the Winners with the given ID provided by User stored in database
    """
    db_winners = WinnersRepo.fetch_by_id(db, winner_id)
    if db_winners is None:
        raise HTTPException(status_code=404, detail="Winners not found with the given ID")
    return db_winners


@app.delete('/winners/{winner_id}', tags=["Winners"])
async def delete_winners(winner_id: int, db: Session = Depends(get_db)):
    """
    Delete the Item with the given ID provided by User stored in database
    """
    db_winners = WinnersRepo.fetch_by_id(db, winner_id)
    if db_winners is None:
        raise HTTPException(status_code=404, detail="Winners not found with the given ID")
    await WinnersRepo.delete(db, winner_id)
    return "Winners deleted successfully!"

@app.get('/intervalsnominatedfilms', tags=["Nominatedfilms"])
async def get_intervals(db: Session = Depends(get_db)) -> dict:
    """
    Obter o produtor com maior intervalo entre dois prêmios consecutivos, e o que
    obteve dois prêmios mais rápido, seguindo a especificação de formato definida na
    página 2
    """
    return count_producers_by_interval(db=db)


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)
