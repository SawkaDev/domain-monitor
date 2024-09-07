# Domain Service API

This API provides endpoints for managing domains in the DNS monitoring system. It allows users to add new domains for monitoring, retrieve all monitored domains, and check the service's health.

## Endpoints

### POST /domain
Add a new domain to monitor.

**Request Body:**
- `domain` (string, required): The domain name to add

**Responses:**
- 201: Domain successfully added
- 400: Invalid input
- 409: Domain already exists
- 500: Server error

### GET /domains
Retrieve all monitored domains.

**Responses:**
- 200: List of all monitored domains
- 500: Server error

### GET /heartbeat
Check if the service is running.

**Responses:**
- 200: Service is running
