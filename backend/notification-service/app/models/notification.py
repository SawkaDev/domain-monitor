from app.extensions import db
from datetime import datetime

class Notification(db.Model):
    __tablename__ = 'notifications'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    domain_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)    
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow) 

    def __init__(self, domain_name, email):
        self.domain_name = domain_name
        self.email = email

    def to_dict(self):
        return {
            'id': self.id,
            'domain_name': self.domain_name,
            'email': self.email,
            'created_at': self.created_at,
            'updated_at': self.updated_at
        }
