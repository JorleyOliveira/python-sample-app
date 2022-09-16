import os
import re
from sqlalchemy.orm import sessionmaker
from app.models import NominatedFilms, Winners, Producers, FilmsProducers
import pandas as pd
from app.db import SessionLocal
from sqlalchemy import func
NAME_FILE_MOVIES = "movies.csv"
STR_SEP_PRODUCERS_NAME = [", ", " and ", ", and "]

def filter_producers_name(name: str):
    return name and name not in STR_SEP_PRODUCERS_NAME

def load_movies(db: sessionmaker = SessionLocal()) -> tuple:

    filepath = os.path.join(os.path.dirname(__file__), '..', NAME_FILE_MOVIES)
    csv_data = pd.read_csv(filepath_or_buffer=filepath, delimiter=";")
    print(csv_data.head())
    filmes = []
    producers = set()
    filmes_producers = {}
    # not_winners = csv_data.loc[csv_data['winner'] != "yes"]
    # for index, row in not_winners.iterrows():
    for index, row in csv_data.iterrows():
        print(row["year"], row["title"], row["studios"], row["producers"], row["winner"])

        data = {"year": row["year"],
                     "title": row["title"],
                     "studios": row["studios"]}
        filmes.append(data)
        print("split")
        print(f"{row['producers']} producers = {re.split('(,|and)', row['producers'])}")
        producers_name = re.split('(, and )|( and )|(, )', row['producers'])
        producers_name = list(filter(filter_producers_name, producers_name))
        producers_name = list(map(str.strip, producers_name))
        producers.update(producers_name)
        print(f"producers_name = {producers_name}")
        filmes_producers[data["title"]] = producers_name


    def create_producer_model(name: str):
        data = {"name": name}
        return Producers(**data)

    producers_map = map(create_producer_model, list(producers))
    producers = list(producers_map)
    db.add_all(producers)

    def create_film_model(data):
        return NominatedFilms(**data)

    film_map = map(create_film_model, filmes)
    films = list(film_map)
    db.add_all(films)
    db.commit()

    films_producers_not_persisted = []
    producers_persisted = {}
    films_persisted = {}
    for k,v in filmes_producers.items():
        film = db.query(NominatedFilms).filter(NominatedFilms.title == k).first()
        films_persisted[k] = film
        for p in v:
            if p not in producers_persisted:
                producers_persisted[p] = db.query(Producers).filter(Producers.name == p).first()
            films_producers_not_persisted.append({"nominatedfilms_id": film.id, "producers_id": producers_persisted[p].id})

    def create_filmsproducers_model(data):
        return FilmsProducers(**data)

    films_producers_map = map(create_filmsproducers_model, films_producers_not_persisted)
    films_producers = list(films_producers_map)
    db.add_all(films_producers)
    db.commit()

    winners_not_persisted = []
    winners_csv = csv_data.loc[csv_data['winner'] == "yes"]
    for index, row in winners_csv.iterrows():
        nominatedFilm = films_persisted.get(row["title"])
        winners_not_persisted.append({"nominatedfilms_id": nominatedFilm.id})

    def create_winners_model(data):
        return Winners(**data)
    winners_map = map(create_winners_model, winners_not_persisted)
    winners = list(winners_map)
    db.add_all(winners)
    db.commit()

    nominated_films_qtd = db.query(NominatedFilms).count()
    winners_qtd = db.query(Winners).count()
    producers_qtd = db.query(Producers).count()
    return nominated_films_qtd, winners_qtd, producers_qtd

def count_producers_by_interval(db: sessionmaker = SessionLocal()):
    """
    SQL exemplo para consulta na base:
    select
        n.title , p.name, max(n."year") as max_year, min(n."year") as min_year, max(n."year") - min(n."year") as interval
    from
        nominatedfilms n
    join winners w on
        n.id = w.nominatedfilms_id
    join filmsproducers f ON
        n.id = f.nominatedfilms_id
    join producers p on
        p.id = f.producers_id

    group by p.name
    --) as t
    HAVING interval > 0
    order by interval

    """
    # Count number of DISTINCT `first_name` values
    records = db.query(Producers.name,
                       func.min((NominatedFilms.year)),
                       func.max((NominatedFilms.year)),
                       func.max((NominatedFilms.year)) - func.min((NominatedFilms.year)))\
        .join(Winners, Winners.nominatedfilms_id == NominatedFilms.id)\
        .join(FilmsProducers, FilmsProducers.nominatedfilms_id == NominatedFilms.id)\
        .join(Producers, Producers.id == FilmsProducers.producers_id)\
        .group_by(Producers.name) \
        .all()
    df = pd.DataFrame(records, columns=['producers', 'previousWin', 'followingWin', 'interval'])
    print(df.head())
    df = df.loc[df['interval'] > 0]
    print(df.head())
    max_interval = df['interval'].max()
    min_interval = df['interval'].min()
    print(min_interval)
    print(max_interval)
    min_objects = []
    max_objects = []
    if max_interval > min_interval:
        min_objects = df.loc[df['interval'] == min_interval].to_json(orient='records')
    if max_interval:
        max_objects = df.loc[df['interval'] == max_interval].to_json(orient='records')
    return {"min": min_objects, "max": max_objects}