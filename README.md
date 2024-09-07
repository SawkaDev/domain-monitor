# Domain Monitor Service

A comprehensive service for tracking and managing DNS records across multiple domains, providing real-time monitoring and historical data tracking.

## Table of Contents
- [Overview](#overview)
- [Features](#features)
- [Architecture](#architecture)
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

For detailed API documentation of each service, please refer to their respective README files:

### Domain Service API

See [Domain Service README](./backend/domain-service/README.md) for full API documentation.

### DNS Service API

See [DNS Service README](./backend/dns-service/README.md) for full API documentation.


## Access Database
- docker exec -it dm-db psql -U user -d dns_service

## Planned Features
- DNS monitoring: A, AAAA, MX, and TXT records
  - Scanning engine (cron)
  - SSL details
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
- Message Queue for distributing monitoring tasks rabbit mq
  - async processing: do not block sender
  - decouple services
  - can easily add more consumers
  - reliable message delivery (persistent queues even if a service fails)
  - load balancing: distribute traffic across multiple consumers
- Caching (redis) 
- Rate limiting
- Input validation / sanitation
