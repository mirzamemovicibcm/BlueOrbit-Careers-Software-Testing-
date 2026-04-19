from pathlib import Path

from flask import Flask

from .api import api_bp
from .db import init_app as init_db_app
from .db import initialize_database
from .views import web_bp


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY="blueorbit-dev-key",
        DATABASE=str(Path(app.instance_path) / "blueorbit.sqlite3"),
        JSON_SORT_KEYS=False,
    )

    if test_config:
        app.config.update(test_config)

    Path(app.instance_path).mkdir(parents=True, exist_ok=True)

    init_db_app(app)

    with app.app_context():
        initialize_database(seed=not app.config.get("TESTING", False))

    app.register_blueprint(web_bp)
    app.register_blueprint(api_bp, url_prefix="/api")

    @app.get("/health")
    def health():
        return {"status": "ok", "app": "BlueOrbit Careers"}

    return app
