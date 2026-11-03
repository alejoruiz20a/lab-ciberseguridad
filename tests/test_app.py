import os
import sys

import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as appmod  # noqa: E402
from init_db import init  # noqa: E402


@pytest.fixture
def client(tmp_path, monkeypatch):
    db = str(tmp_path / "test.db")
    init(db)
    monkeypatch.setattr(appmod, "DB_PATH", db)
    appmod.app.config["TESTING"] = True
    return appmod.app.test_client()


def test_login_ok(client):
    r = client.post("/login", data={"username": "ana", "password": "lab-ana-456"})
    assert r.status_code == 200
    assert "Bienvenido, ana" in r.get_json()["mensaje"]


def test_login_incorrecto(client):
    r = client.post("/login", data={"username": "ana", "password": "mala"})
    assert r.status_code == 401


def test_search_devuelve_resultados(client):
    r = client.get("/search?q=compras")
    assert r.status_code == 200
    assert [n["title"] for n in r.get_json()] == ["Lista de compras"]


def test_greet_nombre_normal(client):
    r = client.get("/greet?name=Ana")
    assert r.status_code == 200
    assert b"Hola, Ana" in r.data


def test_download_valido(client):
    r = client.get("/download?file=nota1.txt")
    assert r.status_code == 200
    assert b"Primera nota" in r.data
    r.close()


def test_download_inexistente(client):
    assert client.get("/download?file=no-existe.txt").status_code == 404


def test_status(client, monkeypatch):
    class Fake:
        status_code = 200

    monkeypatch.setattr(appmod.requests, "get", lambda url, timeout: Fake())
    r = client.get("/status")
    assert r.get_json()["codigo"] == 200
