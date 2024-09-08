# DNS Service

This API provides endpoints for managing and retrieving DNS records for monitored domains. It allows users to get current DNS records, view historical changes, and check the service's health.

## Endpoints

### GET /dns/{domain_id}
Retrieve current DNS records for a specific domain.

**Parameters:**
- `domain_id` (integer, required): The ID of the domain

**Responses:**
- 200: List of current DNS records
- 404: No DNS records found for this domain

### GET /dns/history/{domain_id}
Retrieve DNS history for a specific domain.

**Parameters:**
- `domain_id` (integer, required): The ID of the domain

**Responses:**
- 200: List of historical DNS records
- 404: No DNS history found for this domain

### GET /dns/heartbeat
Check if the service is running.

**Responses:**
- 200: Service is running
