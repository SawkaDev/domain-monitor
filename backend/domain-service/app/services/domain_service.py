from app.models.domain import Domain
from app.extensions import db
from datetime import datetime
import dns.resolver
from flask import current_app
import requests
class DomainService:
    @staticmethod
    def add_entry(domain_name):
        entry = Domain(name=domain_name)
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_domains_paginated(page, limit):
        domains = Domain.query.order_by(Domain.id.desc()).paginate(page=page, per_page=limit, error_out=False)
        total = Domain.query.count()
        return domains.items, total

    @staticmethod
    def get_stats(domain_name):
        entry = Domain.query.filter_by(name=domain_name).first()
        if not entry:
            return None
        
        dns_data = DomainService.get_dns_changes(domain_name)
        whois_data = DomainService.get_whois_changes(domain_name)

        dns_updated_at = datetime.fromisoformat(dns_data.get('updated_at')) if dns_data and dns_data.get('updated_at') else datetime.min
        whois_updated_at = datetime.fromisoformat(whois_data.get('updated_at')) if whois_data and whois_data.get('updated_at') else datetime.min
        most_recent_update = max(dns_updated_at, whois_updated_at)

        return {
            'created_at': entry.created_at.isoformat(),
            'updated_at': most_recent_update.isoformat() if most_recent_update != datetime.min else None,
            'dns_changes': dns_data.get('changes', 0) if dns_data else 0,
            'whois_changes': whois_data.get('changes', 0) if whois_data else 0,
        }

    @staticmethod
    def get_dns_changes(domain_name):
        dns_service_url = 'http://dns-service:5001/api/v1'
        url = f"{dns_service_url}/dns/changes/{domain_name}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            current_app.logger.error(f"Error fetching DNS changes for {domain_name}: {str(e)}")
            return None

    @staticmethod
    def get_whois_changes(domain_name):
        dns_service_url = 'http://whois-service:5002/api/v1'
        url = f"{dns_service_url}/whois/changes/{domain_name}"
        
        try:
            response = requests.get(url, timeout=5)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.RequestException as e:
            current_app.logger.error(f"Error fetching Whois changes for {domain_name}: {str(e)}")
            return None

    @staticmethod
    def domain_exists(domain_name):
        return Domain.query.filter_by(name=domain_name).first()