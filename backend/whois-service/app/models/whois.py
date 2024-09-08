from app.extensions import db
from datetime import datetime

class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    current_whois = db.relationship('CurrentWhois', back_populates='domain', uselist=False, cascade="all, delete-orphan")
    whois_history = db.relationship('WhoisHistory', back_populates='domain', lazy='dynamic', cascade="all, delete-orphan")

    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

    def __repr__(self):
        return f'<Domain {self.name}>'

class CurrentWhois(db.Model):
    __tablename__ = 'current_whois'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False, unique=True, index=True)
    dnssec = db.Column(db.Boolean, default=False)
    registrant_country = db.Column(db.String(255))
    registrant_locality = db.Column(db.String(255))
    registrant_postal_code = db.Column(db.String(255))
    registrant_region = db.Column(db.String(255))
    registrant_street_address = db.Column(db.Text)
    registrant_email = db.Column(db.String(255))
    registrant_name = db.Column(db.String(255))
    registrant_tel = db.Column(db.String(255))
    registrar = db.Column(db.String(255))
    expiration_date = db.Column(db.DateTime)
    last_changed_date = db.Column(db.DateTime)
    name = db.Column(db.String(255))
    nameservers = db.Column(db.Text)
    registration_date = db.Column(db.DateTime)
    status = db.Column(db.Text)
    terms_of_service_url = db.Column(db.Text)
    type = db.Column(db.String(255))
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    domain = db.relationship('Domain', back_populates='current_whois')

    def __init__(self, domain_id, dnssec, registrant_country, registrant_locality, registrant_postal_code,
                 registrant_region, registrant_street_address, registrant_email, registrant_name, registrant_tel,
                 registrar, expiration_date, last_changed_date, name, nameservers, registration_date, status,
                 terms_of_service_url, type):
        self.domain_id = domain_id
        self.dnssec = dnssec
        self.registrant_country = registrant_country
        self.registrant_locality = registrant_locality
        self.registrant_postal_code = registrant_postal_code
        self.registrant_region = registrant_region
        self.registrant_street_address = registrant_street_address
        self.registrant_email = registrant_email
        self.registrant_name = registrant_name
        self.registrant_tel = registrant_tel
        self.registrar = registrar
        self.expiration_date = expiration_date
        self.last_changed_date = last_changed_date
        self.name = name
        self.nameservers = nameservers
        self.registration_date = registration_date
        self.status = status
        self.terms_of_service_url = terms_of_service_url
        self.type = type

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'dnssec': self.dnssec,
            'registrant_country': self.registrant_country,
            'registrant_locality': self.registrant_locality,
            'registrant_postal_code': self.registrant_postal_code,
            'registrant_region': self.registrant_region,
            'registrant_street_address': self.registrant_street_address,
            'registrant_email': self.registrant_email,
            'registrant_name': self.registrant_name,
            'registrant_tel': self.registrant_tel,
            'registrar': self.registrar,
            'expiration_date': self.expiration_date,
            'last_changed_date': self.last_changed_date,
            'name': self.name,
            'nameservers': self.nameservers,
            'registration_date': self.registration_date,
            'status': self.status,
            'terms_of_service_url': self.terms_of_service_url,
            'type': self.type,
            'updated_at': self.updated_at
        }


class WhoisHistory(db.Model):
    __tablename__ = 'whois_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False, index=True)
    field_name = db.Column(db.String(255), nullable=False)
    old_value = db.Column(db.Text)
    new_value = db.Column(db.Text)
    changed_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationship
    domain = db.relationship('Domain', back_populates='whois_history')

    def __init__(self, domain_id, field_name, old_value, new_value):
        self.domain_id = domain_id
        self.field_name = field_name
        self.old_value = old_value
        self.new_value = new_value

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'field_name': self.field_name,
            'old_value': self.old_value,
            'new_value': self.new_value,
            'changed_at': self.changed_at.isoformat() if self.changed_at else None
        }

    def __repr__(self):
        return f'<WhoisHistory {self.domain_id}: {self.field_name}>'