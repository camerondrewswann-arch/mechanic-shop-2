from flask import Flask
from config import Config
from extensions import db, ma, migrate, limiter, cache
from models import Customer, Mechanic, ServiceTicket, Inventory
from blueprints.customers import customer_bp
from blueprints.mechanics import mechanic_bp
from blueprints.service_tickets import service_ticket_bp
from blueprints.inventory import inventory_bp


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    ma.init_app(app)
    migrate.init_app(app, db)
    limiter.init_app(app)
    cache.init_app(app)

    app.register_blueprint(customer_bp, url_prefix="/customers")
    app.register_blueprint(mechanic_bp, url_prefix="/mechanics")
    app.register_blueprint(service_ticket_bp, url_prefix="/service-tickets")
    app.register_blueprint(inventory_bp, url_prefix="/inventory")

    @app.route("/")
    def home():
        return {
            "message": "Mechanic Shop API is running",
            "blueprints": ["/customers", "/mechanics", "/service-tickets", "/inventory"]
        }, 200

    @app.cli.command("init-db")
    def init_db():
        db.create_all()
        print("Database tables created.")

    @app.cli.command("seed")
    def seed_db():
        db.drop_all()
        db.create_all()

        customer = Customer(name="Cameron Swann", email="cameron@example.com", phone="555-123-4567")
        customer.password = "password123"
        mechanic1 = Mechanic(name="Alex Rivera", email="alex@example.com", phone="555-111-2222", specialty="Brakes")
        mechanic2 = Mechanic(name="Jordan Lee", email="jordan@example.com", phone="555-333-4444", specialty="Engine")
        part1 = Inventory(name="Brake Pads", price=89.99)
        part2 = Inventory(name="Oil Filter", price=14.99)
        ticket = ServiceTicket(description="Brake inspection and oil change", status="open", vin="1HGCM82633A004352", customer=customer)
        ticket.mechanics.append(mechanic1)
        ticket.parts.extend([part1, part2])

        db.session.add_all([customer, mechanic1, mechanic2, part1, part2, ticket])
        db.session.commit()
        print("Seed data created. Login with cameron@example.com / password123")

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
