from flask import request
from marshmallow import ValidationError
from sqlalchemy.exc import IntegrityError
from extensions import db, limiter
from models import Customer, ServiceTicket
from utils.auth import encode_token, token_required
from blueprints.customers import customer_bp
from blueprints.customers.schemas import customer_schema, customers_schema, login_schema
from blueprints.service_tickets.schemas import service_tickets_schema


@customer_bp.route("/", methods=["POST"])
def create_customer():
    try:
        data = customer_schema.load(request.get_json() or {})
        db.session.add(data)
        db.session.commit()
        return customer_schema.dump(data), 201
    except ValidationError as err:
        return {"error": "Validation error", "messages": err.messages}, 400
    except IntegrityError:
        db.session.rollback()
        return {"error": "A customer with that email already exists"}, 400


@customer_bp.route("/", methods=["GET"])
@limiter.limit("20 per minute")
def get_customers():
    page = request.args.get("page", 1, type=int)
    per_page = request.args.get("per_page", 5, type=int)
    paginated = Customer.query.paginate(page=page, per_page=per_page, error_out=False)
    return {
        "customers": customers_schema.dump(paginated.items),
        "page": paginated.page,
        "per_page": paginated.per_page,
        "total": paginated.total,
        "pages": paginated.pages
    }, 200


@customer_bp.route("/<int:customer_id>", methods=["PUT"])
@token_required
def update_customer(auth_customer_id, customer_id):
    if auth_customer_id != customer_id:
        return {"error": "You can only update your own customer account"}, 403

    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404

    data = request.get_json() or {}
    for field in ["name", "email", "phone"]:
        if field in data:
            setattr(customer, field, data[field])
    if "password" in data:
        customer.password = data["password"]

    try:
        db.session.commit()
        return customer_schema.dump(customer), 200
    except IntegrityError:
        db.session.rollback()
        return {"error": "Email already in use"}, 400


@customer_bp.route("/<int:customer_id>", methods=["DELETE"])
@token_required
def delete_customer(auth_customer_id, customer_id):
    if auth_customer_id != customer_id:
        return {"error": "You can only delete your own customer account"}, 403

    customer = Customer.query.get(customer_id)
    if not customer:
        return {"error": "Customer not found"}, 404
    db.session.delete(customer)
    db.session.commit()
    return {"message": "Customer deleted successfully"}, 200


@customer_bp.route("/login", methods=["POST"])
def login():
    try:
        data = login_schema.load(request.get_json() or {})
    except ValidationError as err:
        return {"error": "Validation error", "messages": err.messages}, 400

    customer = Customer.query.filter_by(email=data["email"]).first()
    if not customer or not customer.check_password(data["password"]):
        return {"error": "Invalid email or password"}, 401

    return {"token": encode_token(customer.id), "customer": customer_schema.dump(customer)}, 200


@customer_bp.route("/my-tickets", methods=["GET"])
@token_required
def my_tickets(customer_id):
    tickets = ServiceTicket.query.filter_by(customer_id=customer_id).all()
    return service_tickets_schema.dump(tickets), 200
