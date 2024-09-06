# Domain Monitor

# Access database
- docker exec -it dm-db psql -U user -d dns_service

### Planned Features
- DNS monitoring: A, AAAA, MX, and TXT records
  - Scanning engine (cron)
  - SSL details
- WHOIS Data Monitoring: 
  - Registrar details
  - Registration and expiration dates
  - Name servers
  - Registrant information (if available)
- Alert System
  - Email, SMS, webhooks
- UI
  - add domain
  - dns / whois changes
  - update alerts
- Message Queue for distributing monitoring tasks rabbit mq
  - async processing: do not block sender
  - decouple services
  - can easily add more consumers
  - reliable message delivery (persistent queues even if a service fails)
  - load balacning: distribute traffic across multiple consumers
- Caching (redis) 
- Rate limiting
- input validation / sanitation


# DNS Monitoring Service

This is a microservice for monitoring DNS records of domains.

## Setup

1. Clone the repository
2. Create a virtual environment and activate it
3. Install dependencies: `pip install -r requirements.txt`
4. Copy `.env.example` to `.env` and fill in the values
5. Create PostgreSQL databases for development and testing
6. Run migrations: `flask db upgrade`
7. Start the server: `flask run`

## Running with Docker

1. Build the image: `docker-compose build`
2. Start the services: `docker-compose up`

## Running Tests

1. Create a test database in PostgreSQL
2. Set the `TEST_DATABASE_URL` in your `.env` file
3. Run `pytest` in the project root directory

## API Endpoints

- POST /api/v1/dns: Add a new domain to monitor
- GET /api/v1/dns: Get all monitored domains
- GET /api/v1/dns/<domain>: Get DNS records for a specific domain

## Database Migrations

To create a new migration:

