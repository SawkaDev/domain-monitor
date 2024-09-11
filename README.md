# Domain Monitor Service

A comprehensive service for tracking and managing DNS records and WHOIS information across multiple domains, providing real-time monitoring, historical data tracking, and domain validation.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
  - [Technologies Used](#technologies-used)
- [Getting Started](#getting-started)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
- [Configuration](#configuration)
- [API Documentation](#api-documentation)
- [FrontEnd](#frontend)
- [Access Database](#access-database)
- [Planned Features](#planned-features)

## Overview

Domain Monitor offers an easy-to-use platform for managing domain entries, monitoring DNS records and WHOIS information, and accessing historical changes. It's designed for system administrators, network engineers, and anyone needing to keep track of domain-related changes across multiple domains.

## Features

- Add, validate, and manage domains for monitoring
- Retrieve current DNS records and WHOIS information for monitored domains
- Access historical DNS and WHOIS changes
- Real-time updates via message queue system
- RESTful API for easy integration
- Pagination support for efficient data retrieval
- Domain statistics and change tracking
- Notification system for domain changes (frontend feature)

## Architecture

The system is built using a microservices architecture:

<img src="./assets/architecture.JPG" alt="Architecture Diagram" height="400">

1. Domain Service: Manages domain entries, validates domains, and initiates monitoring
2. DNS Service: Tracks and provides current and historical DNS records
3. WHOIS Service: Tracks and provides current and historical WHOIS information
4. Frontend Service: Provides user interface for interacting with the system
5. PostgreSQL Database: Stores domain, DNS record, and WHOIS data
6. RabbitMQ: Handles inter-service communication

### Technologies Used

- Python 3.9+
- Flask: Web framework for building the APIs
- SQLAlchemy: ORM for database interactions
- PostgreSQL: Database for storing domain, DNS, and WHOIS data
- RabbitMQ: Message queue for inter-service communication
- Docker & Docker Compose: Containerization and orchestration
- Next.js: Frontend framework for the user interface
- React Query: Data fetching and state management in the frontend

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL
- RabbitMQ
- Node.js (for frontend development)

### Installation

1. Clone the repository:
   git clone https://github.com/yourusername/domain-monitor.git

2. Navigate to the project directory:
   cd domain-monitor

3. Build and start the services:
   docker-compose up --build

4. For frontend development:
   cd frontend
   npm install
   npm run dev

## Configuration

Environment variables can be set in the `docker-compose.yml` file or in a `.env` file in the project root.

Key variables:
- `DATABASE_URL`: PostgreSQL connection string
- `RABBITMQ_HOST`: RabbitMQ server address
- `SECRET_KEY`: Secret key for Flask applications

## API Documentation

For detailed API documentation, please refer to the following README files:

- [Domain Service README](./backend/domain-service/README.md)
- [DNS Service README](./backend/dns-service/README.md)
- [WHOIS Service README](./backend/whois-service/README.md)

## Frontend

The frontend provides a user-friendly interface for interacting with the Domain Monitor Service. Key features include:

- Domain search and validation
- Comprehensive domain profiles with DNS and WHOIS information
- Historical data visualization
- Notification subscription for domain changes

For more details, see the [Frontend README](./frontend/README.md).

## Planned Features
- SSL Monitoring
- Enhanced Alert System
  - Email, SMS, webhooks
- Caching (Redis) for improved performance
- Rate limiting for API protection
- Export of Historical Data
- Advanced analytics and reporting
- User authentication and personalized watchlists