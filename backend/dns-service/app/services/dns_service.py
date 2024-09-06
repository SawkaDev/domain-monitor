from app.models import DNSEntry
from app.extensions import db
import dns.resolver
from flask import current_app
from datetime import datetime

class DNSService:
    @staticmethod
    def _get_dns_records(domain_name):
        if not domain_name:
            current_app.logger.error(f"Domain {domain_name} not found in the database")
            return None

        timestamp = datetime.now()
        records = []
        for record_type in ['A', 'AAAA', 'MX', 'TXT']:
            try:
                answers = dns.resolver.resolve(domain_name, record_type)
                for rdata in answers:
                    dns_entry = DNSEntry(
                        domain_id=1,
                        record_type=record_type,
                        value=str(rdata),
                        timestamp=timestamp
                    )
                    records.append(dns_entry)
            except Exception as e:
                current_app.logger.error(f"Error fetching {record_type} records for {domain_name}: {str(e)}")

        return records

    @staticmethod
    def update_dns_records(domain_name):
        records = DNSService._get_dns_records(domain_name)
        if records is not None:
            # Add new records
            for record in records:
                db.session.add(record)

            db.session.commit()
            return True
        return False

    @staticmethod
    def get_latest_dns_records(domain_name):
        domain = Domain.query.filter_by(name=domain_name).first()
        if not domain:
            return None

        latest_records = DNSEntry.query.filter_by(domain_id=domain.id).order_by(DNSEntry.timestamp.desc()).all()
        return [record.to_dict() for record in latest_records]
