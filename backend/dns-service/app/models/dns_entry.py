from app.extensions import db
from datetime import datetime

class DNSEntry(db.Model):
    __tablename__ = 'dns_entries'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_id = db.Column(db.Integer, nullable=False)
    record_type = db.Column(db.String(10), nullable=False)
    value = db.Column(db.Text, nullable=False)
    timestamp = db.Column(db.DateTime, nullable=False)
    change_type = db.Column(db.String(10), nullable=False)

    def __init__(self, domain_id, record_type, value, timestamp, change_type='CURRENT'):
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
