from unittest.mock import patch


def test_get_opportunities_returns_json(client):
    response = client.get("/api/opportunities")

    assert response.status_code == 200
    data = response.get_json()
    assert len(data["items"]) == 0


def test_create_opportunity_returns_201_and_saved_payload(client):
    response = client.post(
        "/api/opportunities",
        json={
            "title": "Integration Tester",
            "company": "BlueOrbit Labs",
            "location": "Prishtina",
            "category": "Integration Testing",
            "work_mode": "Hybrid",
            "salary_range": "EUR 1.3k - 2.1k",
            "summary": "Verify modules working together and surface integration risk before release.",
        },
    )

    assert response.status_code == 201
    payload = response.get_json()
    assert payload["title"] == "Integration Tester"
    assert payload["application_count"] == 0


def test_apply_endpoint_returns_201_and_uses_notifier_patch(client):
    create_response = client.post(
        "/api/opportunities",
        json={
            "title": "Mocking Specialist",
            "company": "Orbit QA",
            "location": "Remote",
            "category": "Unit Testing",
            "work_mode": "Remote",
            "salary_range": "EUR 1.2k - 1.9k",
            "summary": "Shape isolated tests with mocks, stubs, and predictable external dependencies.",
        },
    )
    opportunity_id = create_response.get_json()["id"]

    with patch("career_portal.api.send_application_alert") as mocked_alert:
        response = client.post(
            f"/api/opportunities/{opportunity_id}/apply",
            json={
                "applicant_name": "Ari Bloom",
                "applicant_email": "ari@example.com",
                "portfolio_url": "https://ari.dev",
                "motivation": "I write focused tests and use mocks carefully around external services.",
            },
        )

    assert response.status_code == 201
    mocked_alert.assert_called_once()
    assert response.get_json()["applicant_name"] == "Ari Bloom"


def test_apply_endpoint_returns_404_for_missing_opportunity(client):
    response = client.post(
        "/api/opportunities/999/apply",
        json={
            "applicant_name": "Ari Bloom",
            "applicant_email": "ari@example.com",
            "portfolio_url": "https://ari.dev",
            "motivation": "I write focused tests and use mocks carefully around external services.",
        },
    )

    assert response.status_code == 404
    assert response.get_json()["error"] == "Opportunity not found."


def test_invalid_payload_returns_400(client):
    response = client.post(
        "/api/opportunities",
        json={
            "title": "",
            "company": "BlueOrbit Labs",
            "location": "Remote",
            "category": "Unit Testing",
            "work_mode": "Anywhere",
            "salary_range": "EUR 1.2k - 1.9k",
            "summary": "Too short",
        },
    )

    assert response.status_code == 400
    details = response.get_json()["details"]
    assert "title" in details
    assert "work_mode" in details
    assert "summary" in details
