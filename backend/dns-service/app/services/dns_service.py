from flask import current_app
from sqlalchemy.orm import Session
from app.extensions import db
import dns.resolver
from datetime import datetime
from typing import List, Optional
from sqlalchemy.exc import InvalidRequestError

from app.models import DNSEntry

class DNSService:
    @staticmethod
    def _get_dns_records(domain_name: str) -> Optional[List[DNSEntry]]:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return None

        try:
            dns.resolver.resolve(domain_name, 'A')  # Check if domain exists
        except dns.resolver.NXDOMAIN:
            current_app.logger.warning(f"Domain {domain_name} does not exist")
            return None

        timestamp = datetime.now()
        records = []
        for record_type in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA']:
            try:
                answers = dns.resolver.resolve(domain_name, record_type)
                for rdata in answers:
                    dns_entry = DNSEntry(
                        domain_id=None,  # This will be set later
                        record_type=record_type,
                        value=str(rdata),
                        timestamp=timestamp,
                        change_type='CURRENT'
                    )
                    records.append(dns_entry)
            except dns.resolver.NoAnswer:
                current_app.logger.info(f"No {record_type} records found for {domain_name}")
            except Exception as e:
                current_app.logger.error(f"Error fetching {record_type} records for {domain_name}: {str(e)}")

        return records

    @staticmethod
    def _compare_and_store_changes(domain_id: int, current_records: List[DNSEntry]):
        try:
            # Fetch previous records from the database
            previous_records = DNSEntry.query.filter_by(domain_id=domain_id, change_type='CURRENT').all()

            changes = []
            timestamp = datetime.now()

            # Create dictionaries for easier comparison
            current_dict = {(r.record_type, r.value): r for r in current_records}
            previous_dict = {(r.record_type, r.value): r for r in previous_records}

            # Find additions and modifications
            for key, record in current_dict.items():
                if key not in previous_dict:
                    changes.append(DNSEntry(
                        domain_id=domain_id,
                        record_type=record.record_type,
                        value=record.value,
                        timestamp=timestamp,
                        change_type='ADDED'
                    ))
                elif record.value != previous_dict[key].value:
                    changes.append(DNSEntry(
                        domain_id=domain_id,
                        record_type=record.record_type,
                        value=record.value,
                        timestamp=timestamp,
                        change_type='MODIFIED'
                    ))

            # Find deletions
            for key, record in previous_dict.items():
                if key not in current_dict:
                    changes.append(DNSEntry(
                        domain_id=domain_id,
                        record_type=record.record_type,
                        value=record.value,
                        timestamp=timestamp,
                        change_type='DELETED'
                    ))

            # Store changes
            if changes:
                db.session.add_all(changes)

            # Update 'current' records
            DNSEntry.query.filter_by(domain_id=domain_id, change_type='CURRENT').delete()
            for record in current_records:
                record.domain_id = domain_id
                record.change_type = 'CURRENT'
            db.session.add_all(current_records)

        except Exception as e:
            current_app.logger.error(f"Error in _compare_and_store_changes: {str(e)}")
            raise

    @staticmethod
    def update_dns_records(domain_name: str) -> bool:
        try:
            # domain = Domain.query.filter_by(name=domain_name).first()
            if not domain_name:
                current_app.logger.error(f"Domain {domain_name} not found in the database")
                return False

            current_records = DNSService._get_dns_records(domain_name)
            if not current_records:
                current_app.logger.warning(f"No DNS records found for {domain_name}")
                return False

            db.session.begin()
            try:
                # domain.id
                DNSService._compare_and_store_changes(1, current_records)
                db.session.commit()
                return True
            except Exception as e:
                db.session.rollback()
                current_app.logger.error(f"Error in update_dns_records transaction: {str(e)}")
                return False
        except Exception as e:
            current_app.logger.error(f"Error in update_dns_records: {str(e)}")
            return False

    @staticmethod
    def get_dns_history(domain_name: str) -> List[DNSEntry]:
        try:
            domain = Domain.query.filter_by(name=domain_name).first()
            if not domain:
                current_app.logger.error(f"Domain {domain_name} not found in the database")
                return []

            return DNSEntry.query.filter_by(domain_id=domain.id).order_by(DNSEntry.timestamp.desc()).all()
        except Exception as e:
            current_app.logger.error(f"Error in get_dns_history: {str(e)}")
            return []

    @staticmethod
    def get_current_dns_records(domain_name: str) -> List[DNSEntry]:
        try:
            domain = Domain.query.filter_by(name=domain_name).first()
            if not domain:
                current_app.logger.error(f"Domain {domain_name} not found in the database")
                return []

            return DNSEntry.query.filter_by(domain_id=domain.id, change_type='CURRENT').all()
        except Exception as e:
            current_app.logger.error(f"Error in get_current_dns_records: {str(e)}")
            return []