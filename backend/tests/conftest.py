import os
import sys
import pytest
from pathlib import Path

BACKEND_DIR = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(BACKEND_DIR))

os.environ["DB_BACKEND"] = "sqlite"
os.environ["SECRET_KEY"] = "test-secret-fixed-value-for-tests"

from app import app as flask_app
from extensions import db, limiter
from werkzeug.security import generate_password_hash

limiter.enabled = False
from models import (
    User, Country, Destination, Excursion,
    Article, ArticleCategory,
)

@pytest.fixture()
def app():
    flask_app.config.update(
        TESTING=True,
        WTF_CSRF_ENABLED=False,
        RATELIMIT_ENABLED=False,
        SQLALCHEMY_DATABASE_URI="sqlite:///:memory:",
    )
    with flask_app.app_context():
        db.create_all()
        _seed_basic()
        yield flask_app
        db.session.remove()
        db.drop_all()

@pytest.fixture()
def client(app):
    return app.test_client()

@pytest.fixture()
def auth_client(app):
    c = app.test_client()
    r = c.post("/api/auth/login", json={"email": "ivanov@example.com", "password": "password"})
    assert r.status_code == 200, r.get_json()
    return c

@pytest.fixture()
def admin_client(app):
    c = app.test_client()
    r = c.post("/api/auth/login", json={"email": "admin@qsor.ru", "password": "admin123"})
    assert r.status_code == 200, r.get_json()
    return c

def _seed_basic():

    tr = Country(code="TR", name="Турция", is_hot=True)
    eg = Country(code="EG", name="Египет", is_hot=False)
    db.session.add_all([tr, eg])
    db.session.flush()

    antalya = Destination(country_id=tr.id, city="Анталия", slug="antalya",
                          title="Анталия", summary="Курорт", is_featured=True)
    hurghada = Destination(country_id=eg.id, city="Хургада", slug="hurghada",
                           title="Хургада", summary="Красное море")
    db.session.add_all([antalya, hurghada])
    db.session.flush()

    e1 = Excursion(destination_id=antalya.id, slug="kapadokiya",
                   title="Каппадокия за один день", kind="excursion",
                   summary="Долины и церкви", duration="18 часов",
                   price_from=220, languages="русский", is_featured=True)
    e2 = Excursion(destination_id=hurghada.id, slug="reef",
                   title="Дайвинг на рифе", kind="excursion",
                   summary="Коралл", duration="10 часов", price_from=80)
    e3 = Excursion(destination_id=antalya.id, slug="kekova",
                   title="Кекова", kind="excursion",
                   summary="Затонувший город", duration="10 часов",
                   price_from=None)
    db.session.add_all([e1, e2, e3])

    cat = ArticleCategory(slug="industry", name="Индустрия")
    db.session.add(cat)
    db.session.flush()
    a1 = Article(slug="vizy-2026", title="Безвизовые направления",
                 summary="Гайд 2026", body="Текст",
                 category_id=cat.id, is_published=True, is_featured=True)
    db.session.add(a1)

    admin = User(email="admin@qsor.ru",
                 password_hash=generate_password_hash("admin123"),
                 full_name="Администратор", is_admin=True)
    user = User(email="ivanov@example.com",
                password_hash=generate_password_hash("password"),
                full_name="Иванов Сергей", phone="+1 (555) 010-4567")
    user2 = User(email="anna@example.com",
                 password_hash=generate_password_hash("password"),
                 full_name="Громова Анна")
    db.session.add_all([admin, user, user2])
    db.session.commit()
