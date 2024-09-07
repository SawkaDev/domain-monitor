from app.extensions import db
from datetime import datetime

class CurrentDNSRecord(db.Model):
    __tablename__ = 'current_dns_records'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, nullable=False, index=True)
    record_type = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)
    last_updated = db.Column(db.DateTime, nullable=False)

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
            'last_updated': self.last_updated
        }


class DNSEntryHistory(db.Model):
    __tablename__ = 'dns_entry_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, nullable=False, index=True)
    record_type = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    change_type = db.Column(db.String(10), nullable=False)

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
            'timestamp': self.timestamp,
            'change_type': self.change_type
        }