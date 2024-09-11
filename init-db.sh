#!/bin/bash
set -e

# Function to create a database if it doesn't exist
create_db_if_not_exists() {
    database=$1
    if ! psql -U "$POSTGRES_USER" -d postgres -lqt | cut -d \| -f 1 | grep -qw "$database"; then
        psql -U "$POSTGRES_USER" -d postgres -c "CREATE DATABASE $database;"
        echo "Created database: $database"
    else
        echo "Database already exists: $database"
    fi
}

create_db_if_not_exists "domain_service"
create_db_if_not_exists "dns_service"
create_db_if_not_exists "whois_service"
create_db_if_not_exists "notification_service"
