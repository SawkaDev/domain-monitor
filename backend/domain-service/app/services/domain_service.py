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
