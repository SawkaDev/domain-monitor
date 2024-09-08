import whois
from flask import current_app
from sqlalchemy.orm import Session
from app.extensions import db
from datetime import datetime
from typing import List, Optional, Tuple
from app.models.whois import Domain, CurrentWhois, WhoisHistory

class WhoisService:
    @staticmethod
    def _get_whois_data(domain_name: str) -> Optional[dict]:
        if not domain_name:
            current_app.logger.error("Domain name is empty")
            return None

        try:
            w = whois.whois(domain_name)
            return w
        except Exception as e:
            current_app.logger.error(f"Error fetching WHOIS data for {domain_name}: {str(e)}")
            return None

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
                registrar=whois_data['registrar'],
                creation_date=whois_data['creation_date'],
                expiration_date=whois_data['expiration_date'],
                last_updated_date=whois_data['last_updated'],
                name_servers=','.join(whois_data['name_servers']) if whois_data['name_servers'] else None,
                registrant=str(whois_data['registrant']),
                admin=str(whois_data['admin']),
                tech=str(whois_data['tech']),
                billing=str(whois_data['billing'])
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

            timestamp = datetime.now()

            # Check for changes and update history
            for field, new_value in whois_data.items():
                old_value = getattr(current_record, field)
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
