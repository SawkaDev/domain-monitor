import pika
import json
import os
from flask import current_app

def callback(ch, method, properties, body):
    with current_app.app_context():
        message = json.loads(body)
        if message['action'] == 'create_dns_records':
            domain = message['domain']
            domain_id = message['domain_id']

            try:
                from app.services.dns_service import DNSService
                DNSService.create_initial_dns_records(domain, domain_id)
                current_app.logger.info(f"Created initial DNS records for {domain}")
            except Exception as e:
                current_app.logger.error(f"Error creating DNS records for {domain}: {str(e)}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

def start_consuming(app):
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
    rabbitmq_exchange = 'domain_events'

    with app.app_context():
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()

        channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='fanout', durable=True)
        result = channel.queue_declare(queue='', exclusive=True)
        queue_name = result.method.queue
        channel.queue_bind(exchange=rabbitmq_exchange, queue=queue_name)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=queue_name, on_message_callback=callback)
        app.logger.info('DNS service waiting for messages...')
        
        channel.start_consuming()

def init_rabbitmq_consumer(app):
    import threading
    consumer_thread = threading.Thread(target=start_consuming, args=(app,))
    consumer_thread.daemon = True
    consumer_thread.start()
