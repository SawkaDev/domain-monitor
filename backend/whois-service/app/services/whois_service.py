import whoisit
from whoisit import domain as whois_domain
from flask import current_app
from sqlalchemy.orm import Session
from app.extensions import db
from datetime import datetime
from typing import List, Optional, Tuple
from app.models.whois import Domain, CurrentWhois, WhoisHistory
from datetime import datetime
from dateutil import parser
import pytz

class WhoisService:

    _bootstrap_loaded = False

    @staticmethod
    def _load_bootstrap():
        if not WhoisService._bootstrap_loaded:
            try:
                whoisit.bootstrap()
                WhoisService._bootstrap_loaded = True
                current_app.logger.info("WHOIS bootstrap data loaded successfully")
            except Exception as e:
                current_app.logger.error(f"Error loading WHOIS bootstrap data: {str(e)}")

    @staticmethod
    def _get_whois_data(domain_name: str) -> Optional[dict]:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return None

        WhoisService._load_bootstrap()

        try:
            result = whois_domain(domain_name)
            
            registrar = result.get('entities', {}).get('registrar', [{}])[0]
            registrant = result.get('entities', {}).get('registrant', [{}])[0]

            whois_dict = {
                'dnssec': result.get('dnssec', False),
                'registrant_country': registrant.get('address', {}).get('country'),
                'registrant_locality': registrant.get('address', {}).get('locality'),
                'registrant_postal_code': registrant.get('address', {}).get('postal_code'),
                'registrant_region': registrant.get('address', {}).get('region'),
                'registrant_street_address': registrant.get('address', {}).get('street_address'),
                'registrant_email': registrant.get('email'),
                'registrant_name': registrant.get('name'),
                'registrant_tel': registrant.get('tel'),
                'registrar': registrar.get('name'),
                'expiration_date': result.get('expiration_date'),
                'last_changed_date': result.get('last_changed_date'),
                'name': result.get('name'),
                'nameservers': ','.join(ns.rstrip('.') for ns in result.get('nameservers', [])),
                'registration_date': result.get('registration_date'),
                'status': ','.join(result.get('status', [])),
                'terms_of_service_url': result.get('terms_of_service_url'),
                'type': result.get('type')
            }

            return whois_dict
        except Exception as e:
            current_app.logger.error(f"Error fetching WHOIS data for {domain_name}: {str(e)}")
            return None

    @staticmethod
    def create_or_get_domain(domain_name: str, domain_id: int) -> Tuple[Domain, bool]:
        session = db.session
        try:
            domain = Domain.query.filter_by(id=domain_id).first()
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
    def create_initial_whois_record(domain_name: str, domain_id: int) -> bool:
        if not domain_name or not domain_id:
            current_app.logger.error("Domain name is empty or domain ID is empty")
            return False

        domain, is_new = WhoisService.create_or_get_domain(domain_name, domain_id)
        if not domain:
            current_app.logger.error(f"Failed to create or get domain for {domain_name}")
            return False
        if not is_new:
            current_app.logger.error(f"Initial WHOIS record already created for {domain_name}")
            return False

        whois_data = WhoisService._get_whois_data(domain_name)
        if not whois_data:
            current_app.logger.warning(f"No WHOIS data found for {domain_name}")
            return False

        session = db.session
        try:
            new_record = CurrentWhois(
                domain_id=domain_id,
                **whois_data
            )
            session.add(new_record)
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            current_app.logger.error(f"Error in create_initial_whois_record: {str(e)}")
            return False

    @staticmethod
    def update_whois_record(domain_name: str) -> bool:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return False

        domain = Domain.query.filter_by(name=domain_name).first()
        if not domain:
            current_app.logger.error(f"Domain {domain_name} not found in database")
            return False

        whois_data = WhoisService._get_whois_data(domain_name)
        if not whois_data:
            current_app.logger.warning(f"No WHOIS data found for {domain_name}")
            return False

        session = db.session
        try:
            current_record = CurrentWhois.query.filter_by(domain_id=domain.id).first()
            if not current_record:
                current_app.logger.error(f"No current WHOIS record found for {domain_name}")
                return False

            timestamp = datetime.now(pytz.utc)

            def normalize_datetime(dt):
                if dt is None:
                    return None
                if isinstance(dt, str):
                    dt = parser.parse(dt)
                if dt.tzinfo is None:
                    dt = pytz.utc.localize(dt)
                else:
                    dt = dt.astimezone(pytz.utc)
                return dt.replace(tzinfo=None)  # Remove timezone info for comparison

            def format_for_storage(dt):
                if dt is None:
                    return None
                if dt.tzinfo is None:
                    dt = pytz.utc.localize(dt)
                return dt.isoformat()

            # Check for changes and update history
            for field, new_value in whois_data.items():
                old_value = getattr(current_record, field)
                # Handle date fields
                if field in ['registration_date', 'expiration_date', 'last_changed_date']:
                    old_value_normalized = normalize_datetime(old_value)
                    new_value_normalized = normalize_datetime(new_value)
                    
                    if old_value_normalized != new_value_normalized:
                        session.add(WhoisHistory(
                            domain_id=domain.id,
                            field_name=field,
                            old_value=format_for_storage(old_value),
                            new_value=format_for_storage(new_value),
                            changed_at=timestamp
                        ))
                        setattr(current_record, field, new_value)
                else:
                    # Handle non-date fields
                    if old_value != new_value:
                        session.add(WhoisHistory(
                            domain_id=domain.id,
                            field_name=field,
                            old_value=str(old_value),
                            new_value=str(new_value),
                            changed_at=timestamp
                        ))
                        setattr(current_record, field, new_value)

            current_record.updated_at = timestamp
            session.commit()
            return True
        except Exception as e:
            session.rollback()
            current_app.logger.error(f"Error in update_whois_record: {str(e)}")
            return False

    @staticmethod
    def get_whois_history(domain: str) -> List[WhoisHistory]:
        try:
            domain = Domain.query.filter_by(name=domain).first()
            if not domain:
                current_app.logger.error(f"Domain {domain} not found in database")
                return []
            return WhoisHistory.query.filter_by(domain_id=domain.id).order_by(WhoisHistory.changed_at.desc()).all()
        except Exception as e:
            current_app.logger.error(f"Error in get_whois_history: {str(e)}")
            return []

    @staticmethod
    def get_current_whois_record(domain: str) -> Optional[CurrentWhois]:
        try:
            domain = Domain.query.filter_by(name=domain).first()
            if not domain:
                current_app.logger.error(f"Domain {domain} not found in database")
                return None
            return CurrentWhois.query.filter_by(domain_id=domain.id).first()
        except Exception as e:
            current_app.logger.error(f"Error in get_current_whois_record: {str(e)}")
            return None
