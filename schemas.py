# Mechanic Shop Advanced API

A Flask REST API for managing a mechanic shop. This project includes customers, mechanics, service tickets, inventory parts, token authentication, rate limiting, caching, pagination, and many-to-many relationships.

## Features

- Customer CRUD and login
- JWT-style token authentication using `python-jose`
- Protected `/customers/my-tickets` route
- Mechanic CRUD
- Service ticket CRUD
- Assign/remove mechanics from service tickets
- Advanced service ticket edit route with `add_ids` and `remove_ids`
- Inventory CRUD
- Add/remove inventory parts from service tickets
- Mechanic ranking endpoint by most tickets worked
- Pagination on customer list
- Rate limiting with Flask-Limiter
- Caching with Flask-Caching
- Exported Postman collection included

## Tech Stack

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Marshmallow
- Flask-Migrate
- Flask-Limiter
- Flask-Caching
- python-jose
- SQLite by default

## Setup

```bash
python -m venv venv
```

### Windows

```bash
venv\Scripts\activate
```

### Mac/Linux

```bash
source venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Create and seed the database:

```bash
flask --app app.py seed
```

Run the app:

```bash
flask --app app.py run --debug
```

The API will run at:

```text
http://127.0.0.1:5000
```

## Seed Login

Use this customer account after running the seed command:

```text
Email: cameron@example.com
Password: password123
```

## Authentication

Login:

```http
POST /customers/login
```

Body:

```json
{
  "email": "cameron@example.com",
  "password": "password123"
}
```

Copy the returned token and use it in protected routes:

```text
Authorization: Bearer YOUR_TOKEN_HERE
```

## Main Endpoints

### Customers

| Method | Endpoint | Description |
|---|---|---|
| POST | `/customers/` | Create customer |
| GET | `/customers/?page=1&per_page=5` | List customers with pagination |
| PUT | `/customers/<id>` | Update customer, token required |
| DELETE | `/customers/<id>` | Delete customer, token required |
| POST | `/customers/login` | Login and get token |
| GET | `/customers/my-tickets` | Get logged-in customer's tickets, token required |

### Mechanics

| Method | Endpoint | Description |
|---|---|---|
| POST | `/mechanics/` | Create mechanic |
| GET | `/mechanics/` | List mechanics, cached |
| PUT | `/mechanics/<id>` | Update mechanic |
| DELETE | `/mechanics/<id>` | Delete mechanic |
| GET | `/mechanics/most-tickets` | Mechanics ordered by most service tickets |

### Service Tickets

| Method | Endpoint | Description |
|---|---|---|
| POST | `/service-tickets/` | Create service ticket |
| GET | `/service-tickets/` | List service tickets |
| GET | `/service-tickets/<id>` | Get one service ticket |
| PUT | `/service-tickets/<id>` | Update service ticket |
| DELETE | `/service-tickets/<id>` | Delete service ticket |
| PUT | `/service-tickets/<ticket_id>/assign-mechanic/<mechanic_id>` | Add mechanic to ticket |
| PUT | `/service-tickets/<ticket_id>/remove-mechanic/<mechanic_id>` | Remove mechanic from ticket |
| PUT | `/service-tickets/<ticket_id>/edit` | Add/remove multiple mechanics |
| PUT | `/service-tickets/<ticket_id>/add-part/<part_id>` | Add inventory part to ticket |
| PUT | `/service-tickets/<ticket_id>/remove-part/<part_id>` | Remove inventory part from ticket |

### Inventory

| Method | Endpoint | Description |
|---|---|---|
| POST | `/inventory/` | Create inventory part |
| GET | `/inventory/` | List inventory, cached |
| GET | `/inventory/<id>` | Get one inventory part |
| PUT | `/inventory/<id>` | Update inventory part |
| DELETE | `/inventory/<id>` | Delete inventory part |

## Postman

Import this file into Postman:

```text
postman/mechanic_shop_advanced_api_collection.json
```

## GitHub Submission

Upload this whole folder to GitHub. Submit your GitHub repository URL and your short presentation video directly to Disco.
