# DNS Monitoring API

## Endpoints

### POST /domain
Add a new domain to monitor.

**Parameters:**
- `domain` (string, required): The domain name to add

**Responses:**
- 201: Domain successfully added
- 400: Invalid input
- 409: Domain already exists
- 500: Server error

### GET /domains
Retrieve all monitored domains.

**Responses:**
- 200: List of all domains
- 500: Server error
