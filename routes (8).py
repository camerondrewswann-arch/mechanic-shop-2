from marshmallow import fields
from extensions import ma
from models import Mechanic


class MechanicSchema(ma.SQLAlchemyAutoSchema):
    ticket_count = fields.Method("get_ticket_count", dump_only=True)

    class Meta:
        model = Mechanic
        load_instance = True
        include_relationships = True

    def get_ticket_count(self, obj):
        return len(obj.service_tickets)


mechanic_schema = MechanicSchema()
mechanics_schema = MechanicSchema(many=True)
