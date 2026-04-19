from flask import Blueprint, jsonify, request

from .db import get_db
from .notifier import send_application_alert
from .repositories import CareerRepository
from .services import NotFoundError
from .services import ValidationError
from .services import create_opportunity
from .services import submit_application


api_bp = Blueprint("api", __name__)


def _repo():
    return CareerRepository(get_db())


@api_bp.get("/opportunities")
def list_opportunities():
    repo = _repo()
    return jsonify({"items": repo.list_opportunities()})


@api_bp.get("/opportunities/<int:opportunity_id>")
def get_opportunity(opportunity_id):
    repo = _repo()
    opportunity = repo.get_opportunity(opportunity_id)
    if opportunity is None:
        return jsonify({"error": "Opportunity not found."}), 404
    return jsonify(opportunity)


@api_bp.post("/opportunities")
def create_opportunity_api():
    repo = _repo()
    payload = request.get_json(silent=True) or {}
    try:
        opportunity = create_opportunity(repo, payload)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed.", "details": exc.errors}), 400
    return jsonify(opportunity), 201


@api_bp.get("/applications")
def list_applications():
    repo = _repo()
    return jsonify({"items": repo.list_applications()})


@api_bp.post("/opportunities/<int:opportunity_id>/apply")
def apply_api(opportunity_id):
    repo = _repo()
    payload = request.get_json(silent=True) or {}
    try:
        application = submit_application(repo, opportunity_id, payload, send_application_alert)
    except ValidationError as exc:
        return jsonify({"error": "Validation failed.", "details": exc.errors}), 400
    except NotFoundError as exc:
        return jsonify({"error": str(exc)}), 404
    return jsonify(application), 201
