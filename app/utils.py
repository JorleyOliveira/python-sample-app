import os
from sqlalchemy.orm import sessionmaker
from app.models import NominatedFilms, Winners
import pandas as pd
from app.db import SessionLocal
from sqlalchemy import func
NAME_FILE_MOVIES = "movies.csv"


def load_movies(db: sessionmaker = SessionLocal()) -> tuple:
    filepath = os.path.join(os.path.dirname(__file__), '..', NAME_FILE_MOVIES)
    csv_data = pd.read_csv(filepath_or_buffer=filepath, delimiter=";")
    print(csv_data.head())
    data = []
    not_winners = csv_data.loc[csv_data['winner'] != "yes"]
    for index, row in not_winners.iterrows():
        print(row["year"], row["title"], row["studios"], row["producers"], row["winner"])

        data.append({"year": row["year"],
                     "title": row["title"],
                     "studios": row["studios"],
                     "producers": row["producers"]})

    def create_film_model(data):
        return NominatedFilms(**data)

    film_map = map(create_film_model, data)
    films = list(film_map)
    db.add_all(films)
    db.commit()

    winners = csv_data.loc[csv_data['winner'] == "yes"]
    for index, row in winners.iterrows():
        data = {"year": row["year"],
                "title": row["title"],
                "studios": row["studios"],
                "producers": row["producers"]}
        nominatedFilm = NominatedFilms(**data)
        db.add(nominatedFilm)
        db.commit()
        db.refresh(nominatedFilm)
        data_winners = {"nominatedfilms_id": nominatedFilm.id}
        db.add(Winners(**data_winners))
        db.commit()

    nominated_films_qtd = db.query(NominatedFilms).count()
    winners_qtd = db.query(Winners).count()
    return nominated_films_qtd, winners_qtd

def count_producers_by_interval(db: sessionmaker = SessionLocal()):
    # Count number of DISTINCT `first_name` values
    records = db.query(NominatedFilms.producers,
                       func.min((NominatedFilms.year)),
                       func.max((NominatedFilms.year)),
                       func.max((NominatedFilms.year)) - func.min((NominatedFilms.year)))\
        .join(Winners, Winners.nominatedfilms_id == NominatedFilms.id)\
        .group_by(NominatedFilms.producers) \
        .all()
    df = pd.DataFrame(records, columns=['producers', 'previousWin', 'followingWin', 'interval'])
    print(df.head())
    df = df.loc[df['interval'] > 0]
    print(df.head())
    min_interval = df['interval'].max()
    max_interval = df['interval'].min()
    print(min_interval)
    print(max_interval)
    min_objects = []
    max_objects = []
    if max_interval > min_interval:
        min_objects = df.loc[df['interval'] == min_interval].to_json(orient='records')
    if max_interval:
        max_objects = df.loc[df['interval'] == max_interval].to_json(orient='records')
    return {"min": min_objects, "max": max_objects}