from app import schemas
from app.utils import load_movies, count_producers_by_interval

def test_load_movies(session):
    nominated_films_qtd, winners_qtd = load_movies(db=session)
    assert nominated_films_qtd == 206
    assert winners_qtd == 42

def test_count_producers_by_interval(test_load_movies, session):
    producers = count_producers_by_interval(db=session)
    assert {
        "min": [],
        "max": "[{\"producers\":\"Bo Derek\",\"previousWin\":1984,\"followingWin\":1990,\"interval\":6}]"
    } == producers

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
