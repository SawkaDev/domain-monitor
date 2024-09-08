from app.extensions import db
from datetime import datetime

class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    current_whois = db.relationship('CurrentWhois', back_populates='domain', uselist=False)
    whois_history = db.relationship('WhoisHistory', back_populates='domain', lazy='dynamic')

    def __init__(self, name, id):
        self.name = name
        self.id = id
        
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }

class CurrentWhois(db.Model):
    __tablename__ = 'current_whois'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False, unique=True, index=True)
    registrar = db.Column(db.String(255))
    registrant_name = db.Column(db.String(255))
    registrant_organization = db.Column(db.String(255))
    registrant_email = db.Column(db.String(255))
    admin_email = db.Column(db.String(255))
    tech_email = db.Column(db.String(255))
    name_servers = db.Column(db.Text)
    creation_date = db.Column(db.DateTime)
    expiration_date = db.Column(db.DateTime)
    last_updated_date = db.Column(db.DateTime)
    raw_data = db.Column(db.Text)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationship
    domain = db.relationship('Domain', back_populates='current_whois')

    def __init__(self, domain_id, registrar, registrant_name, registrant_organization, registrant_email,
                 admin_email, tech_email, name_servers, creation_date, expiration_date, last_updated_date, raw_data):
        self.domain_id = domain_id
        self.registrar = registrar
        self.registrant_name = registrant_name
        self.registrant_organization = registrant_organization
        self.registrant_email = registrant_email
        self.admin_email = admin_email
        self.tech_email = tech_email
        self.name_servers = name_servers
        self.creation_date = creation_date
        self.expiration_date = expiration_date
        self.last_updated_date = last_updated_date
        self.raw_data = raw_data

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'registrar': self.registrar,
            'registrant_name': self.registrant_name,
            'registrant_organization': self.registrant_organization,
            'registrant_email': self.registrant_email,
            'admin_email': self.admin_email,
            'tech_email': self.tech_email,
            'name_servers': self.name_servers,
            'creation_date': self.creation_date,
            'expiration_date': self.expiration_date,
            'last_updated_date': self.last_updated_date,
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
            'changed_at': self.changed_at
        }
