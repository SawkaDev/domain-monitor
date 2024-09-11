# API Gateway

## Overview

This API Gateway serves as a central entry point for our microservices architecture. It's built using Flask and incorporates several key features to enhance performance, security, and scalability.

Key Features:
- Request forwarding to appropriate microservices
- Caching using Redis for improved response times
- Rate limiting to prevent abuse and ensure fair usage
- Logging and request tracking for monitoring and debugging

## Technologies Used

- Flask 2.3.2: A lightweight WSGI web application framework
- Flask-Limiter 2.7.0: For implementing rate limiting
- Redis: For caching and supporting rate limiting
- Requests: For forwarding HTTP requests to microservices
