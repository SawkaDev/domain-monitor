from app.extensions import db
from datetime import datetime

class Domain(db.Model):
    __tablename__ = 'domains'

    id = db.Column(db.Integer, primary_key=True, nullable=False, autoincrement=False)
    name = db.Column(db.String(255), unique=True, nullable=False, index=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    current_dns_records = db.relationship('CurrentDNSRecord', back_populates='domain', lazy='dynamic')
    dns_entry_history = db.relationship('DNSEntryHistory', back_populates='domain', lazy='dynamic')

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

class CurrentDNSRecord(db.Model):
    __tablename__ = 'current_dns_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False, index=True)
    record_type = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)

    # Relationship
    domain = db.relationship('Domain', back_populates='current_dns_records')

    def __init__(self, domain_id, record_type, value, last_updated):
        self.domain_id = domain_id
        self.record_type = record_type
        self.value = value
        self.last_updated = last_updated

    def to_dict(self):
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'record_type': self.record_type,
            'value': self.value,
            'last_updated': self.last_updated.isoformat() if self.last_updated else None
        }

    def __repr__(self):
        return f'<CurrentDNSRecord {self.domain_id}: {self.record_type}>'

class DNSEntryHistory(db.Model):
    __tablename__ = 'dns_entry_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, db.ForeignKey('domains.id'), nullable=False, index=True)
    record_type = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    change_type = db.Column(db.String(10), nullable=False)

    # Relationship
    domain = db.relationship('Domain', back_populates='dns_entry_history')

    def __init__(self, domain_id, record_type, value, timestamp, change_type):
        self.domain_id = domain_id
        self.record_type = record_type
        self.value = value
        self.timestamp = timestamp
        self.change_type = change_type

    def to_dict(self):  
        return {
            'id': self.id,
            'domain_id': self.domain_id,
            'record_type': self.record_type,
            'value': self.value,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'change_type': self.change_type
        }

    def __repr__(self):
        return f'<DNSEntryHistory {self.domain_id}: {self.record_type} - {self.change_type}>'
