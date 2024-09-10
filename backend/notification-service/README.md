# Notification Service

This API provides endpoints for managing domain notifications. It allows users to subscribe to domain updates, unsubscribe from notifications, and retrieve notification information. The service integrates with other services REST API's for adding and deleteing notificaitons and RabbitMQ for automated notifications and handles sending email notifications (currently mocked).

## Endpoints

### GET /notifications
Retrieve all notifications.

**Responses:**
- **200**: List of notifications
- **200**: Empty list if no notifications found

### GET /notifications/user/{email}
Retrieve notifications for a specific user.

**Parameters:**
- `email`: User's email address

**Responses:**
- **200**: List of user notifications
- **200**: Empty list if no notifications found

### POST /notification
Add a new notification subscription.

**Request Body:**
```json
{
  "domain_name": "example.com",
  "email": "user@example.com"
}
```

**Responses:**
- **201**: Notification added
- **400**: Invalid input
- **409**: Notification already exists

### DELETE /notification
Remove a notification subscription.

**Request Body:**
```json
{
  "domain_name": "example.com",
  "email": "user@example.com"
}
```

**Responses:**
- **200**: Notification removed
- **400**: Invalid input
- **404**: Notification not found

### GET /heartbeat
Check if the service is running.

**Responses:**
- **200**: Service is running

## Usage

To use this API, send HTTP requests to the endpoints. For example:
- `GET /notifications`
- `GET /notifications/user/user@example.com`
- `POST /notification`
- `DELETE /notification`
- `GET /heartbeat`

## Error Handling

The API uses standard HTTP status codes to indicate success or failure. Errors return a JSON response with an error message.

## Data Format

All responses are in JSON format. Notifications are returned as objects or arrays of objects.
