# Domain Monitor Service

A comprehensive service for tracking and managing DNS records across multiple domains, providing real-time monitoring and historical data tracking.

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
- [Access Database](#access-database)
- [Planned Features](#planned-features)

## Overview

Domain Monitor offers an easy-to-use platform for managing domain entries, monitoring DNS records, and accessing historical changes. It's designed for system administrators, network engineers, and anyone needing to keep track of DNS changes across multiple domains.

## Features

- Add and manage domains for monitoring
- Retrieve current DNS records for monitored domains
- Access historical DNS changes (10 minute updates)
- Real-time updates via message queue system
- RESTful API for easy integration

## Architecture

The system is built using a microservices architecture:

1. Domain Service: Manages domain entries and initiates monitoring
2. DNS Service: Tracks and provides current and historical DNS records
3. PostgreSQL Database: Stores domain and DNS record data
4. RabbitMQ: Handles inter-service communication

### Technologies Used

- Python 3.9+
- Flask: Web framework for building the APIs
- SQLAlchemy: ORM for database interactions
- PostgreSQL: Database for storing domain and DNS data
- RabbitMQ: Message queue for inter-service communication
- Docker & Docker Compose: Containerization and orchestration

## Getting Started

### Prerequisites

- Docker and Docker Compose
- Python 3.9+
- PostgreSQL
- RabbitMQ

### Installation

1. Clone the repository:
   git clone https://github.com/yourusername/domain-monitor.git

2. Navigate to the project directory:
   cd domain-monitor

3. Build and start the services:
   docker-compose up --build

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

## Planned Features
- SSL Monitoring
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
- Caching (redis) 
- Rate limiting
- Input validation / sanitation
