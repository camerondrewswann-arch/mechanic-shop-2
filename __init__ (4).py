from marshmallow import fields, validate
from extensions import ma
from models import Customer


class CustomerSchema(ma.SQLAlchemyAutoSchema):
    password = fields.String(load_only=True, required=True, validate=validate.Length(min=4))

    class Meta:
        model = Customer
        load_instance = True
        include_fk = True
        exclude = ("password_hash",)


class LoginSchema(ma.Schema):
    email = fields.Email(required=True)
    password = fields.String(required=True)


customer_schema = CustomerSchema()
customers_schema = CustomerSchema(many=True)
login_schema = LoginSchema()
