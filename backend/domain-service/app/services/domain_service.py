from app.models.domain import Domain
from app.extensions import db
import dns.resolver
from flask import current_app

class DomainService:
    @staticmethod
    def add_entry(domain_name):
        entry = Domain(name=domain_name)
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_all_domains():
        return Domain.query.all()

    @staticmethod
    def get_stats(domain_name):
        entry = Domain.query.filter_by(name=domain_name).first()
        if not entry:
            return None
        
        return {
            'created_at': entry.created_at.isoformat(),
            'updated_at': entry.updated_at.isoformat(),
            'dns_changes': 10,
            'whois_changes': 5
        }