from app.models.notification import Notification
from app.extensions import db

class NotificationService:
    @staticmethod
    def add_notification(domain_name, email):
        notification = Notification(domain_name=domain_name, email=email)
        db.session.add(notification)
        db.session.commit()
        return notification

    @staticmethod
    def remove_notification(domain_name, email):
        notification = Notification.query.filter_by(domain_name=domain_name, email=email).first()
        if notification:
            db.session.delete(notification)
            db.session.commit()
            return True
        return False

    @staticmethod
    def get_notifications_for_user(email):
        notifications = Notification.query.filter_by(email=email).order_by(Notification.id.desc()).all()
        return notifications

    @staticmethod
    def get_all_notifications():
        notifications = Notification.query.order_by(Notification.id.desc()).all()
        return notifications

    @staticmethod
    def user_has_notification(domain_name, email):
        notification = Notification.query.filter_by(domain_name=domain_name, email=email).first()
        return notification is not None
