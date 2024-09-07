from flask import current_app
from sqlalchemy.orm import Session
from app.extensions import db
import dns.resolver
from dns.exception import DNSException
from datetime import datetime
from typing import List, Optional, Tuple
from sqlalchemy.exc import InvalidRequestError
from app.models.dns_entry import Domain

from app.models import CurrentDNSRecord, DNSEntryHistory

class DNSService:
    @staticmethod
    def _get_dns_records(domain_name: str) -> Optional[List[dict]]:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return None

        records = []
        full_domain = domain_name.rstrip('.')
        for record_type in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA']:
            try:
                answers = dns.resolver.resolve(full_domain, record_type)
                for rdata in answers:
                    value = str(rdata)
                    # if record_type == 'MX':
                    #     value = "CHANGED VALUE"
                    records.append({
                        'record_type': record_type,
                        'value': value
                    })
            except dns.resolver.NoAnswer:
                current_app.logger.info(f"No {record_type} records found for {full_domain}")
            except dns.resolver.NXDOMAIN:
                current_app.logger.warning(f"Domain {full_domain} does not exist")
                break
            except dns.exception.Timeout:
                current_app.logger.error(f"Timeout while fetching {record_type} records for {full_domain}")
            except DNSException as e:
                current_app.logger.error(f"DNS error fetching {record_type} records for {full_domain}: {str(e)}")
            except Exception as e:
                current_app.logger.error(f"Unexpected error fetching {record_type} records for {full_domain}: {str(e)}")

        if not records:
            current_app.logger.warning(f"No DNS records found for {domain_name}")
            return None

        return records

    @staticmethod
    def create_or_get_domain(domain_name: str, domain_id: int) -> Tuple[Domain, bool]:
        session = db.session
        try:
            domain = Domain.query.filter_by(id=domain_id, name=domain_name).first()
            if domain:
                return domain, False
            
            new_domain = Domain(id=domain_id, name=domain_name)
            session.add(new_domain)
            session.commit()
            return new_domain, True
        except Exception as e:
            session.rollback()
            current_app.logger.error(f"Error in create_or_get_domain: {str(e)}")
            return None, False

    @staticmethod
    def create_initial_dns_records(domain_name: str, domain_id: int) -> bool:
        if not domain_name or not domain_id:
            current_app.logger.error("Domain name is empty or domain ID is empty")
            return False

        domain, is_new = DNSService.create_or_get_domain(domain_name, domain_id)
        if not domain:
            current_app.logger.error(f"Failed to create or get domain for {domain_name}")
            return False
        if not is_new:
            current_app.logger.error(f"Inital DNS records already created for {domain_name}")
            return False

        current_records = DNSService._get_dns_records(domain_name)
        if not current_records:
            current_app.logger.warning(f"No DNS records found for {domain_name}")
            return False

        session = db.session
        try:
            timestamp = datetime.now()

            for record in current_records:
                new_record = CurrentDNSRecord(
                    domain_id=domain_id,
                    record_type=record['record_type'],
                    value=record['value'],
                    last_updated=timestamp
                )
                session.add(new_record)

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            current_app.logger.error(f"Error in create_initial_dns_records: {str(e)}")
            return False

    @staticmethod
    def update_dns_records(domain_name: str) -> bool:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return False

        domain = Domain.query.filter_by(name=domain_name).first()
        if not domain:
            current_app.logger.error(f"Domain {domain_name} not found in database")
            return False

        current_records = DNSService._get_dns_records(domain_name)
        if not current_records:
            current_app.logger.warning(f"No DNS records found for {domain_name}")
            return False

        session = db.session
        try:
            # Fetch existing current records
            existing_records = CurrentDNSRecord.query.filter_by(domain_id=domain.id).all()
            
            # Create sets for existing and current records
            existing_set = {(r.record_type, r.value) for r in existing_records}
            current_set = {(r['record_type'], r['value']) for r in current_records}

            timestamp = datetime.now()

            # Find additions
            additions = current_set - existing_set
            for record_type, value in additions:
                new_record = CurrentDNSRecord(
                    domain_id=domain.id,
                    record_type=record_type,
                    value=value,
                    last_updated=timestamp
                )
                session.add(new_record)
                session.add(DNSEntryHistory(
                    domain_id=domain.id,
                    record_type=record_type,
                    value=value,
                    timestamp=timestamp,
                    change_type='ADDED'
                ))

            # Find deletions
            deletions = existing_set - current_set
            for record_type, value in deletions:
                record_to_delete = next(r for r in existing_records if r.record_type == record_type and r.value == value)
                session.delete(record_to_delete)
                session.add(DNSEntryHistory(
                    domain_id=domain.id,
                    record_type=record_type,
                    value=value,
                    timestamp=timestamp,
                    change_type='DELETED'
                ))

            session.commit()
            return True
        except Exception as e:
            session.rollback()
            current_app.logger.error(f"Error in update_dns_records: {str(e)}")
            return False

    @staticmethod
    def get_dns_history(domain_id: int) -> List[DNSEntryHistory]:
        try:
            domain = Domain.query.filter_by(id=domain_id).first()
            if not domain:
                current_app.logger.error(f"Domain {domain_id} not found in database")
                return []
            return DNSEntryHistory.query.filter_by(domain_id=domain.id).order_by(DNSEntryHistory.timestamp.desc()).all()
        except Exception as e:
            current_app.logger.error(f"Error in get_dns_history: {str(e)}")
            return []

    @staticmethod
    def get_current_dns_records(domain_id: int) -> List[CurrentDNSRecord]:
        try:
            domain = Domain.query.filter_by(id=domain_id).first()
            if not domain:
                current_app.logger.error(f"Domain {domain_id} not found in database")
                return []
            return CurrentDNSRecord.query.filter_by(domain_id=domain.id).all()
        except Exception as e:
            current_app.logger.error(f"Error in get_current_dns_records: {str(e)}")
            return []
