import sqlite3

from flask import current_app, g


SEED_OPPORTUNITIES = [
    {
        "title": "QA Automation Engineer",
        "company": "BlueOrbit Labs",
        "location": "Prishtina",
        "category": "Quality Engineering",
        "work_mode": "Hybrid",
        "salary_range": "EUR 1.4k - 2.1k",
        "summary": "Design resilient test flows, improve release confidence, and keep product quality sharp.",
    },
    {
        "title": "Frontend Tester",
        "company": "Northline Studio",
        "location": "Remote",
        "category": "UI Testing",
        "work_mode": "Remote",
        "salary_range": "EUR 1.2k - 1.8k",
        "summary": "Own browser journeys, accessibility checks, and feedback loops for polished interfaces.",
    },
    {
        "title": "API Quality Analyst",
        "company": "Pulse Grid",
        "location": "Skopje",
        "category": "Backend Testing",
        "work_mode": "On-site",
        "salary_range": "EUR 1.5k - 2.4k",
        "summary": "Stress REST endpoints, validate payload accuracy, and harden error handling for core services.",
    },
]


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(current_app.config["DATABASE"])
        g.db.row_factory = sqlite3.Row
        g.db.execute("PRAGMA foreign_keys = ON")
    return g.db


def close_db(_error=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    with current_app.open_resource("schema.sql") as schema:
        db.executescript(schema.read().decode("utf-8"))
    db.commit()


def initialize_database(seed=True):
    db = get_db()
    table_exists = db.execute(
        """
        SELECT name
        FROM sqlite_master
        WHERE type = 'table' AND name = 'opportunities'
        """
    ).fetchone()

    if table_exists is None:
        init_db()

    if seed:
        total_rows = db.execute("SELECT COUNT(*) FROM opportunities").fetchone()[0]
        if total_rows == 0:
            db.executemany(
                """
                INSERT INTO opportunities
                    (title, company, location, category, work_mode, salary_range, summary)
                VALUES
                    (:title, :company, :location, :category, :work_mode, :salary_range, :summary)
                """,
                SEED_OPPORTUNITIES,
            )
            db.commit()


def init_app(app):
    app.teardown_appcontext(close_db)
