from flask import jsonify, request, current_app
from app.api.v1 import bp
from app.services.domain_service import DomainService
from sqlalchemy.exc import IntegrityError
import pika
import json
import os

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_queue = 'domain_registration'

def send_message(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
    channel = connection.channel()
    channel.queue_declare(queue=rabbitmq_queue, durable=True)
    channel.basic_publish(
        exchange='',
        routing_key=rabbitmq_queue,
        body=json.dumps(message),
        properties=pika.BasicProperties(delivery_mode=2)
    )
    connection.close()

@bp.route('/domain', methods=['POST'])
def add_dns_entry():
    data = request.json
    if not data or 'domain' not in data:
        return jsonify({'error': 'Invalid input'}), 400

    domain_name = data['domain']
    try:
        result = DomainService.add_entry(domain_name)

        send_message({
            'action': 'create_dns_records',
            'domain': domain_name,
            'domain_id': result.id
        })

        return jsonify(result.to_dict()), 201
    except IntegrityError:
        return jsonify({'error': 'Domain already exists'}), 409
    except Exception as e:
        current_app.logger.error(f"Error adding domain: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/domains', methods=['GET'])
def get_all_domains():
    try:
        domains = DomainService.get_all_domains()
        return jsonify([domain.to_dict() for domain in domains]), 200
    except Exception as e:
        current_app.logger.error(f"Error retrieving domains: {str(e)}")
        return jsonify({'error': 'An unexpected error occurred'}), 500

@bp.route('/heartbeat', methods=['GET'])
def heartbeat():
    return jsonify({'status': 'ok'}), 200
