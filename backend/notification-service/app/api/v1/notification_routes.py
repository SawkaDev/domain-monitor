from flask import jsonify, request, current_app
from app.api.v1 import bp
from app.services.notification_service import NotificationService
from sqlalchemy.exc import IntegrityError

@bp.route('/all', methods=['GET'])
def get_all_notifications():
    try:
        notifications = NotificationService.get_all_notifications()
        return jsonify({
            'notifications': [notification.to_dict() for notification in notifications]
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving notifications: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/all/user/<string:email>', methods=['GET'])
def get_user_notifications(email):
    try:
        notifications = NotificationService.get_notifications_for_user(email)
        return jsonify({
            'notifications': [notification.to_dict() for notification in notifications]
        }), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving user notifications: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500
        

@bp.route('/', methods=['POST'])
def add_notification():
    data = request.json
    if not data or 'domain_name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    domain_name = data['domain_name']
    email = data['email']
    
    try:
        if NotificationService.user_has_notification(domain_name, email):
            return jsonify({'error': 'Notification already exists'}), 409
        
        notification = NotificationService.add_notification(domain_name, email)
        return jsonify(notification.to_dict()), 201
    except Exception as e:
        current_app.logger.error(f"Error adding notification: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/', methods=['DELETE'])
def remove_notification():
    data = request.json
    if not data or 'domain_name' not in data or 'email' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    domain_name = data['domain_name']
    email = data['email']
    
    try:
        if NotificationService.remove_notification(domain_name, email):
            return jsonify({'message': 'Notification removed successfully'}), 200
        else:
            return jsonify({'error': 'Notification not found'}), 404
    except Exception as e:
        current_app.logger.error(f"Error removing notification: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200
