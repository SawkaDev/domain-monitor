# DNS Service

This API provides endpoints for managing and retrieving DNS records for monitored domains. It allows users to get current DNS records, view historical changes, update DNS records, and check the service's health.

## Endpoints

### GET /{domain}
Retrieve current DNS records for a specific domain.

**Parameters:**
- `domain` (string, required): The domain name

**Responses:**
- 200: List of current DNS records
- 200: Empty list if no records found

### GET /history/{domain}
Retrieve DNS history for a specific domain.

**Parameters:**
- `domain` (string, required): The domain name

**Responses:**
- 200: List of historical DNS records
- 200: Empty list if no history found

### POST /{domain_name}
Update DNS records for a specific domain. (Helper route for manual updates)

**Parameters:**
- `domain_name` (string, required): The domain name

**Responses:**
- 200: Update successful
- 500: Update failed

### GET /heartbeat
Check if the service is running.

**Responses:**
- 200: Service is running

### GET /changes/{domain}
Retrieve DNS changes for a specific domain.

**Parameters:**
- `domain` (string, required): The domain name

**Responses:**
- 200: DNS changes information
- 404: Domain not found

## Usage

To use this API, send HTTP requests to the appropriate endpoints. For example:

GET /example.com
GET /history/example.com
POST /example.com
GET /heartbeat
GET /changes/example.com

## Error Handling

The API uses standard HTTP status codes to indicate the success or failure of requests. In case of errors, a JSON response with an error message will be returned.

## Data Format

All responses are in JSON format. DNS records and history entries are returned as arrays of objects, each containing relevant information about the DNS record or change.

## Notes

- The POST endpoint for updating DNS records is currently a helper route and may be replaced by a scheduled task in the future.
- Ensure proper error handling and input validation when integrating with this API.