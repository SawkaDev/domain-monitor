# WHOIS Service

This API provides endpoints for managing and retrieving WHOIS records for monitored domains. It allows users to get current WHOIS records, view historical changes, update WHOIS records, and check the service's health.

## Endpoints

### GET /whois/{domain}
Retrieve the current WHOIS record for a specific domain.

**Parameters:**
- `domain` (string, required): The domain name

**Responses:**
- 200: Current WHOIS record
- 200: Empty object if no record found

### GET /whois/history/{domain}
Retrieve WHOIS history for a specific domain.

**Parameters:**
- `domain` (string, required): The domain name

**Responses:**
- 200: List of historical WHOIS records
- 200: Empty list if no history found

### POST /whois/{domain_name}
Update WHOIS record for a specific domain. (Manual trigger, may be removed in the future)

**Parameters:**
- `domain_name` (string, required): The domain name

**Responses:**
- 200: Update successful
- 500: Update failed

### GET /whois/heartbeat
Check if the service is running.

**Responses:**
- 200: Service is running

### POST /whois/create/{domain}
Create an initial WHOIS record for a domain.

**Parameters:**
- `domain` (string, required): The domain name
- Request body: JSON object with `domain_id` (integer, required)

**Responses:**
- 200: Creation successful
- 400: Missing domain_id
- 500: Creation failed

### GET /whois/changes/{domain}
Retrieve WHOIS changes for a specific domain.

**Parameters:**
- `domain` (string, required): The domain name

**Responses:**
- 200: WHOIS changes information
- 404: Domain not found

## Usage

To use this API, send HTTP requests to the appropriate endpoints. For example:

GET /whois/example.com
GET /whois/history/example.com
POST /whois/example.com
GET /whois/heartbeat
POST /whois/create/example.com
GET /whois/changes/example.com

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. In case of errors, a JSON response with an error message will be returned.

## Data Format

All responses are in JSON format. WHOIS records and history entries are returned as objects or arrays of objects, each containing relevant information about the WHOIS record or change.

## Notes

- The POST endpoint for updating WHOIS records is currently a manual trigger and may be removed in the future.
- The create endpoint requires a domain_id to be provided in the request body.
- Ensure proper error handling and input validation when integrating with this API.