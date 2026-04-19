# BlueOrbit Careers

BlueOrbit Careers is a Flask and SQLite web application created for the Software Testing course assignment. It focuses on managing career opportunities and candidate applications through both HTML routes and REST API endpoints.

## What is included

- A modern black-and-blue dashboard UI for posting and applying to roles
- A REST API for opportunity and application workflows
- Automated unit, integration, system, and API tests
- Mock and patch usage for isolated dependency testing
- A verified test run with 15 passing tests
- A detailed testing report in `docs/testing-report.md`

## Project structure

```text
career_portal/
  __init__.py
  api.py
  db.py
  notifier.py
  repositories.py
  schema.sql
  services.py
  static/
  templates/
docs/
tests/
app.py
```

## Run locally

```bash
python app.py
```

The application will start on `http://127.0.0.1:5000`.

## Run the tests

```bash
python -m pytest
```

## API routes

- `GET /api/opportunities`
- `GET /api/opportunities/<id>`
- `POST /api/opportunities`
- `GET /api/applications`
- `POST /api/opportunities/<id>/apply`

## Notes

- The assignment PDF filename says `2025-2026`, but the brief inside the document states `Academic Year: 2024/2025`.
- Seed opportunities are created automatically for the normal app so the dashboard is not empty on first launch.
- The test environment uses a clean temporary database without seed data.
