from app.extensions import db
from datetime import datetime

class DNSEntry(db.Model):
    __tablename__ = 'dns_entries'

    id = db.Column(db.Integer, primary_key=True)
    domain = db.Column(db.String(255), unique=True, nullable=False, index=True)
    records = db.Column(db.JSON, nullable=False)
    last_checked = db.Column(db.DateTime(timezone=True), default=datetime.utcnow, index=True)

    def __repr__(self):
        return f'<DNSEntry {self.domain}>'
