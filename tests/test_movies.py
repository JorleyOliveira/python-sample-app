from app import schemas
from app.utils import load_movies, count_producers_by_interval

def test_load_movies(session):
    nominated_films_qtd, winners_qtd, producers_qtd = load_movies(db=session)
    assert nominated_films_qtd == 206
    assert winners_qtd == 42
    assert producers_qtd == 359

def test_count_producers_by_interval(test_load_movies, session):
    producers = count_producers_by_interval(db=session)
    assert {'min': '[{"producers":"Joel Silver","previousWin":1990,"followingWin":1991,"interval":1}]',
            'max': '[{"producers":"Matthew Vaughn","previousWin":2002,"followingWin":2015,"interval":13}]'} == producers

def test_get_all_nominatedfilms(test_load_movies, client):
    res = client.get("/nominatedfilms/")

    def validate(post):
        return schemas.NominatedFilms(**post)
    nominatedfilms_map = map(validate, res.json())
    nominatedfilms_list = list(nominatedfilms_map)
    # api with limit 100
    assert len(res.json()) == 100 
    assert len(res.json()) == len(nominatedfilms_list)
    assert res.status_code == 200

def test_get_all_winners(test_load_movies, client):
    res = client.get("/winners/")

    def validate(post):
        return schemas.Winners(**post)
    winners_map = map(validate, res.json())
    winners_list = list(winners_map)
    # api with limit 100
    assert len(res.json()) == 42
    assert len(res.json()) == len(winners_list)
    assert res.status_code == 200

def test_get_all_producers(test_load_movies, client):
    res = client.get("/producers/")

    def validate(post):
        return schemas.Producers(**post)
    producers_map = map(validate, res.json())
    producers_list = list(producers_map)
    # api with limit 100
    assert len(res.json()) == 100
    assert len(res.json()) == len(producers_list)
    assert res.status_code == 200

def test_get_all_filmsproducers(test_load_movies, client):
    res = client.get("/filmsproducers/")

    def validate(post):
        return schemas.FilmsProducers(**post)
    filmsproducers_map = map(validate, res.json())
    filmsproducers_list = list(filmsproducers_map)
    # api with limit 100
    assert len(res.json()) == 100
    assert len(res.json()) == len(filmsproducers_list)
    assert res.status_code == 200
