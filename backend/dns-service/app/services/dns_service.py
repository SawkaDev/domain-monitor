from flask import current_app
from sqlalchemy.orm import Session
from app.extensions import db
import dns.resolver
from dns.exception import DNSException
from datetime import datetime
from typing import List, Optional
from sqlalchemy.exc import InvalidRequestError

from app.models import CurrentDNSRecord, DNSEntryHistory

class DNSService:
    @staticmethod
    def _get_dns_records(domain_name: str) -> Optional[List[dict]]:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return None

        records = []
        subdomains = ['', 'www.']  # Check both root domain and www subdomain

        for subdomain in subdomains:
            full_domain = f"{subdomain}{domain_name}".rstrip('.')
            for record_type in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA']:
                try:
                    answers = dns.resolver.resolve(full_domain, record_type)
                    for rdata in answers:
                        value = str(rdata)
                        if record_type == 'MX':
                            value = "MATT"  # Override MX record value
                        records.append({
                            'subdomain': subdomain,
                            'record_type': record_type,
                            'value': value
                        })
                except dns.resolver.NoAnswer:
                    current_app.logger.info(f"No {record_type} records found for {full_domain}")
                except dns.resolver.NXDOMAIN:
                    current_app.logger.warning(f"Domain {full_domain} does not exist")
                    break  # Stop checking other record types for this subdomain
                except dns.exception.Timeout:
                    current_app.logger.error(f"Timeout while fetching {record_type} records for {full_domain}")
                except DNSException as e:
                    current_app.logger.error(f"DNS error fetching {record_type} records for {full_domain}: {str(e)}")
                except Exception as e:
                    current_app.logger.error(f"Unexpected error fetching {record_type} records for {full_domain}: {str(e)}")

        if not records:
            current_app.logger.warning(f"No DNS records found for {domain_name} or its www subdomain")
            return None

        return records

    @staticmethod
    def create_initial_dns_records(domain_name: str) -> bool:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return False

        current_records = DNSService._get_dns_records(domain_name)
        if not current_records:
            current_app.logger.warning(f"No DNS records found for {domain_name}")
            return False

        domain_id = 1  # Hardcoded for now, replace with actual domain_id later

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
                session.add(DNSEntryHistory(
                    domain_id=domain_id,
                    record_type=record['record_type'],
                    value=record['value'],
                    timestamp=timestamp,
                    change_type='INITIAL'
                ))

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

        current_records = DNSService._get_dns_records(domain_name)
        if not current_records:
            current_app.logger.warning(f"No DNS records found for {domain_name}")
            return False

        domain_id = 1  # Hardcoded for now, replace with actual domain_id later

        session = db.session
        try:
            # Fetch existing current records
            existing_records = CurrentDNSRecord.query.filter_by(domain_id=domain_id).all()
            existing_dict = {(r.record_type, r.value): r for r in existing_records}

            timestamp = datetime.now()

            # Update current records and track changes
            for record in current_records:
                key = (record['record_type'], record['value'])
                full_domain = f"{record['subdomain']}{domain_name}".rstrip('.')
                if key not in existing_dict:
                    # New record
                    new_record = CurrentDNSRecord(
                        domain_id=domain_id,
                        record_type=record['record_type'],
                        value=record['value'],
                        last_updated=timestamp
                    )
                    session.add(new_record)
                    session.add(DNSEntryHistory(
                        domain_id=domain_id,
                        record_type=record['record_type'],
                        value=record['value'],
                        timestamp=timestamp,
                        change_type='ADDED'
                    ))
                elif existing_dict[key].value != record['value']:
                    # Modified record
                    existing_dict[key].value = record['value']
                    existing_dict[key].last_updated = timestamp
                    session.add(DNSEntryHistory(
                        domain_id=domain_id,
                        record_type=record['record_type'],
                        value=record['value'],
                        timestamp=timestamp,
                        change_type='MODIFIED'
                    ))

            # Check for deleted records
            current_keys = set((r['record_type'], r['value']) for r in current_records)
            for key, record in existing_dict.items():
                if key not in current_keys:
                    session.delete(record)
                    session.add(DNSEntryHistory(
                        domain_id=domain_id,
                        record_type=record.record_type,
                        value=record.value,
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
    def get_dns_history(domain_name: str) -> List[DNSEntryHistory]:
        try:
            domain_id = 1  # Hardcoded for now, replace with actual domain_id later
            return DNSEntryHistory.query.filter_by(domain_id=domain_id).order_by(DNSEntryHistory.timestamp.desc()).all()
        except Exception as e:
            current_app.logger.error(f"Error in get_dns_history: {str(e)}")
            return []

    @staticmethod
    def get_current_dns_records(domain_name: str) -> List[CurrentDNSRecord]:
        try:
            domain_id = 1  # Hardcoded for now, replace with actual domain_id later
            return CurrentDNSRecord.query.filter_by(domain_id=domain_id).all()
        except Exception as e:
            current_app.logger.error(f"Error in get_current_dns_records: {str(e)}")
            return []
