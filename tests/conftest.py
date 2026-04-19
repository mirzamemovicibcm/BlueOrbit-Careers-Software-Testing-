from pathlib import Path
from uuid import uuid4

import pytest

from career_portal import create_app
from career_portal.db import get_db
from career_portal.repositories import CareerRepository


@pytest.fixture()
def app():
    runtime_dir = Path(__file__).resolve().parents[1] / "tests_runtime"
    runtime_dir.mkdir(exist_ok=True)
    database_path = runtime_dir / f"test-{uuid4().hex}.sqlite3"
    app = create_app(
        {
            "TESTING": True,
            "DATABASE": str(database_path),
            "SECRET_KEY": "test-key",
        }
    )
    yield app
    database_path.unlink(missing_ok=True)


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def repo(app):
    with app.app_context():
        yield CareerRepository(get_db())
