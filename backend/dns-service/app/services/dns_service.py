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
        full_domain = domain_name.rstrip('.')
        for record_type in ['A', 'AAAA', 'MX', 'TXT', 'NS', 'CNAME', 'SOA', 'PTR', 'SRV', 'CAA']:
            try:
                answers = dns.resolver.resolve(full_domain, record_type)
                for rdata in answers:
                    value = str(rdata)
                    if record_type == 'NS':
                        value = "matt.com"  # Override MX record value for testing
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
            
            # Group existing records by record type
            existing_dict = {}
            for record in existing_records:
                if record.record_type not in existing_dict:
                    existing_dict[record.record_type] = []
                existing_dict[record.record_type].append(record)

            timestamp = datetime.now()

            # Group current records by record type
            current_dict = {}
            for record in current_records:
                if record['record_type'] not in current_dict:
                    current_dict[record['record_type']] = []
                current_dict[record['record_type']].append(record['value'])

            # Compare and update records
            for record_type, current_values in current_dict.items():
                if record_type in existing_dict:
                    existing_values = [r.value for r in existing_dict[record_type]]
                    
                    # Check for modifications and additions
                    for value in current_values:
                        if value in existing_values:
                            existing_values.remove(value)
                        else:
                            # New value for existing record type
                            new_record = CurrentDNSRecord(
                                domain_id=domain_id,
                                record_type=record_type,
                                value=value,
                                last_updated=timestamp
                            )
                            session.add(new_record)
                            session.add(DNSEntryHistory(
                                domain_id=domain_id,
                                record_type=record_type,
                                value=value,
                                timestamp=timestamp,
                                change_type='ADDED'
                            ))
                    
                    # Remaining values in existing_values have been removed
                    for value in existing_values:
                        record_to_delete = next(r for r in existing_dict[record_type] if r.value == value)
                        session.delete(record_to_delete)
                        session.add(DNSEntryHistory(
                            domain_id=domain_id,
                            record_type=record_type,
                            value=value,
                            timestamp=timestamp,
                            change_type='DELETED'
                        ))
                else:
                    # Entirely new record type
                    for value in current_values:
                        new_record = CurrentDNSRecord(
                            domain_id=domain_id,
                            record_type=record_type,
                            value=value,
                            last_updated=timestamp
                        )
                        session.add(new_record)
                        session.add(DNSEntryHistory(
                            domain_id=domain_id,
                            record_type=record_type,
                            value=value,
                            timestamp=timestamp,
                            change_type='ADDED'
                        ))

            # Check for deleted record types
            for record_type in existing_dict.keys():
                if record_type not in current_dict:
                    for record in existing_dict[record_type]:
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
