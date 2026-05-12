{
  "info": {
    "name": "Mechanic Shop Advanced API",
    "schema": "https://schema.getpostman.com/json/collection/v2.1.0/collection.json",
    "description": "Postman collection for testing customers, mechanics, service tickets, inventory, auth, caching, rate limiting, and advanced queries."
  },
  "variable": [
    { "key": "base_url", "value": "http://127.0.0.1:5000" },
    { "key": "token", "value": "" }
  ],
  "item": [
    {
      "name": "Health Check",
      "request": { "method": "GET", "url": "{{base_url}}/" }
    },
    {
      "name": "Customers",
      "item": [
        {
          "name": "Create Customer",
          "request": {
            "method": "POST",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"name\": \"New Customer\",\n  \"email\": \"newcustomer@example.com\",\n  \"phone\": \"555-999-0000\",\n  \"password\": \"password123\"\n}" },
            "url": "{{base_url}}/customers/"
          }
        },
        {
          "name": "Login Customer",
          "event": [
            {
              "listen": "test",
              "script": {
                "exec": [
                  "const json = pm.response.json();",
                  "if (json.token) { pm.collectionVariables.set('token', json.token); }"
                ],
                "type": "text/javascript"
              }
            }
          ],
          "request": {
            "method": "POST",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"email\": \"cameron@example.com\",\n  \"password\": \"password123\"\n}" },
            "url": "{{base_url}}/customers/login"
          }
        },
        {
          "name": "Get Customers Paginated",
          "request": { "method": "GET", "url": "{{base_url}}/customers/?page=1&per_page=5" }
        },
        {
          "name": "Get My Tickets Protected",
          "request": {
            "method": "GET",
            "header": [{ "key": "Authorization", "value": "Bearer {{token}}" }],
            "url": "{{base_url}}/customers/my-tickets"
          }
        },
        {
          "name": "Update Customer Protected",
          "request": {
            "method": "PUT",
            "header": [
              { "key": "Authorization", "value": "Bearer {{token}}" },
              { "key": "Content-Type", "value": "application/json" }
            ],
            "body": { "mode": "raw", "raw": "{\n  \"phone\": \"555-222-3333\"\n}" },
            "url": "{{base_url}}/customers/1"
          }
        }
      ]
    },
    {
      "name": "Mechanics",
      "item": [
        {
          "name": "Create Mechanic",
          "request": {
            "method": "POST",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"name\": \"Taylor Brooks\",\n  \"email\": \"taylor@example.com\",\n  \"phone\": \"555-123-9999\",\n  \"specialty\": \"Transmission\"\n}" },
            "url": "{{base_url}}/mechanics/"
          }
        },
        {
          "name": "Get Mechanics Cached",
          "request": { "method": "GET", "url": "{{base_url}}/mechanics/" }
        },
        {
          "name": "Update Mechanic",
          "request": {
            "method": "PUT",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"specialty\": \"Electrical\"\n}" },
            "url": "{{base_url}}/mechanics/1"
          }
        },
        {
          "name": "Mechanics By Most Tickets",
          "request": { "method": "GET", "url": "{{base_url}}/mechanics/most-tickets" }
        }
      ]
    },
    {
      "name": "Inventory",
      "item": [
        {
          "name": "Create Part",
          "request": {
            "method": "POST",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"name\": \"Spark Plug\",\n  \"price\": 12.99\n}" },
            "url": "{{base_url}}/inventory/"
          }
        },
        {
          "name": "Get Inventory Cached",
          "request": { "method": "GET", "url": "{{base_url}}/inventory/" }
        },
        {
          "name": "Get One Part",
          "request": { "method": "GET", "url": "{{base_url}}/inventory/1" }
        },
        {
          "name": "Update Part",
          "request": {
            "method": "PUT",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"price\": 19.99\n}" },
            "url": "{{base_url}}/inventory/1"
          }
        }
      ]
    },
    {
      "name": "Service Tickets",
      "item": [
        {
          "name": "Create Ticket",
          "request": {
            "method": "POST",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"description\": \"Replace spark plugs\",\n  \"status\": \"open\",\n  \"vin\": \"TESTVIN123\",\n  \"customer_id\": 1\n}" },
            "url": "{{base_url}}/service-tickets/"
          }
        },
        {
          "name": "Get Tickets",
          "request": { "method": "GET", "url": "{{base_url}}/service-tickets/" }
        },
        {
          "name": "Update Ticket",
          "request": {
            "method": "PUT",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"status\": \"in progress\"\n}" },
            "url": "{{base_url}}/service-tickets/1"
          }
        },
        {
          "name": "Assign Mechanic",
          "request": { "method": "PUT", "url": "{{base_url}}/service-tickets/1/assign-mechanic/2" }
        },
        {
          "name": "Remove Mechanic",
          "request": { "method": "PUT", "url": "{{base_url}}/service-tickets/1/remove-mechanic/2" }
        },
        {
          "name": "Edit Mechanics Add and Remove IDs",
          "request": {
            "method": "PUT",
            "header": [{ "key": "Content-Type", "value": "application/json" }],
            "body": { "mode": "raw", "raw": "{\n  \"add_ids\": [2],\n  \"remove_ids\": []\n}" },
            "url": "{{base_url}}/service-tickets/1/edit"
          }
        },
        {
          "name": "Add Part To Ticket",
          "request": { "method": "PUT", "url": "{{base_url}}/service-tickets/1/add-part/1" }
        },
        {
          "name": "Remove Part From Ticket",
          "request": { "method": "PUT", "url": "{{base_url}}/service-tickets/1/remove-part/1" }
        }
      ]
    }
  ]
}
