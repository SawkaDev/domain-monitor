from app.models import DNSEntry
from app.extensions import db
import dns.resolver
from flask import current_app

class DNSService:
    @staticmethod
    def add_entry(domain):
        records = DNSService._get_dns_records(domain)
        entry = DNSEntry(domain=domain, records=records)
        db.session.add(entry)
        db.session.commit()
        return entry

    @staticmethod
    def get_all_entries(page, per_page):
        return DNSEntry.query.paginate(page=page, per_page=per_page, error_out=False)

    @staticmethod
    def get_entry(domain):
        return DNSEntry.query.filter_by(domain=domain).first()

    @staticmethod
    def _get_dns_records(domain):
        records = {}
        for record_type in ['A', 'AAAA', 'MX', 'TXT']:
            try:
                answers = dns.resolver.resolve(domain, record_type)
                records[record_type] = [str(rdata) for rdata in answers]
            except Exception as e:
                current_app.logger.error(f"Error fetching {record_type} records for {domain}: {str(e)}")
                records[record_type] = []
        return records
