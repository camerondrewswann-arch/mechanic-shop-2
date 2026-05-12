from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from extensions import db, cache, limiter
from models import Mechanic
from blueprints.mechanics import mechanic_bp
from blueprints.mechanics.schemas import mechanic_schema, mechanics_schema


@mechanic_bp.route("/", methods=["POST"])
def create_mechanic():
    try:
        mechanic = mechanic_schema.load(request.get_json() or {})
        db.session.add(mechanic)
        db.session.commit()
        cache.delete("mechanics_list")
        return mechanic_schema.dump(mechanic), 201
    except ValidationError as err:
        return {"error": "Validation error", "messages": err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {"error": "A mechanic with that email already exists"}, 400


@mechanic_bp.route("/", methods=["GET"])
@cache.cached(timeout=60, key_prefix="mechanics_list")
def get_mechanics():
    mechanics = Mechanic.query.all()
    return mechanics_schema.dump(mechanics), 200


@mechanic_bp.route("/<int:mechanic_id>", methods=["PUT"])
def update_mechanic(mechanic_id):
    mechanic = Mechanic.query.get(mechanic_id)
    if not mechanic:
        return {"error": "Mechanic not found"}, 404

    data = request.get_json() or {}
    for field in ["name", "email", "phone", "specialty"]:
        if field in data:
            setattr(mechanic, field, data[field])

    try:
        db.session.commit()
        cache.delete("mechanics_list")
        return mechanic_schema.dump(mechanic), 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already in use"}, 400


@mechanic_bp.route("/<int:mechanic_id>", methods=["DELETE"])
def delete_mechanic(mechanic_id):
    mechanic = Mechanic.query.get(mechanic_id)
    if not mechanic:
        return {"error": "Mechanic not found"}, 404
    db.session.delete(mechanic)
    db.session.commit()
    cache.delete("mechanics_list")
    return {"message": "Mechanic deleted successfully"}, 200


@mechanic_bp.route("/most-tickets", methods=["GET"])
@limiter.limit("10 per minute")
def mechanics_by_ticket_count():
    mechanics = Mechanic.query.all()
    mechanics.sort(key=lambda item: len(item.service_tickets), reverse=True)
    return mechanics_schema.dump(mechanics), 200
