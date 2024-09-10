# Domain Service API

This API provides endpoints for managing domains in the DNS monitoring system. It allows users to validate and add new domains for monitoring, retrieve monitored domains with pagination, get domain stats, and check the service's health.

## Endpoints

### GET /domains
Retrieve monitored domains with pagination.

**Query Parameters:**
- `page` (integer, optional): Page number for pagination (default: 1)
- `limit` (integer, optional): Number of domains per page (default: 20)

**Responses:**
- 200: List of monitored domains with pagination info
  {
    "domains": [{ ... }],
    "total": 100,
    "page": 1,
    "limit": 20
  }
- 500: Server error

### GET /domain/stats/{domain_name}
Retrieve statistics for a specific domain.

**Parameters:**
- `domain_name` (string, required): The domain name

**Responses:**
- 200: Domain statistics
- 404: Domain not found
- 500: Server error

### GET /heartbeat
Check if the service is running.

**Responses:**
- 200: Service is running

### POST /domain/validate
Validate a domain and add it for monitoring if it doesn't exist.

**Request Body:**
- `domain` (string, required): The domain name to validate/add

**Responses:**
- 200: Domain exists
  {
    "exists": true,
    "records_ready": true
  }
- 201: Domain added
  {
    "exists": true,
    "added": true,
    "records_ready": false
  }
- 400: Invalid input
- 500: Server error

## Usage

To use this API, send HTTP requests to the appropriate endpoints. For example:

GET /domains?page=1&limit=20
GET /domain/stats/example.com
GET /heartbeat
POST /domain/validate

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. In case of errors, a JSON response with an error message will be returned.

## Data Format

All responses are in JSON format. Domain information and statistics are returned as objects or arrays of objects, containing relevant information about the domains.

## Notes

- The validate endpoint will add the domain for monitoring if it doesn't exist and trigger the creation of DNS records.
- Pagination is implemented for retrieving domains to handle large datasets efficiently.
- Ensure proper error handling and input validation when integrating with this API.