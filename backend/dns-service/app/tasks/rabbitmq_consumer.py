import pika
import json
import os
import time
from flask import current_app

def callback(ch, method, properties, body):
    with current_app.app_context():
        try:
            message = json.loads(body)
            if message['action'] == 'create_dns_records':
                domain = message['domain']
                domain_id = message['domain_id']

                from app.services.dns_service import DNSService
                success = DNSService.create_initial_dns_records(domain, domain_id)
                if success:
                    current_app.logger.info(f"Created initial DNS records for {domain}")
                else:
                    current_app.logger.error(f"Error creating initial DNS records for {domain}")
            else:
                current_app.logger.warning(f"Unknown action received: {message['action']}")
        except json.JSONDecodeError:
            current_app.logger.error("Received invalid JSON message")
        except KeyError as e:
            current_app.logger.error(f"Missing key in message: {str(e)}")
        except Exception as e:
            current_app.logger.error(f"Error processing message: {str(e)}")

    ch.basic_ack(delivery_tag=method.delivery_tag)

def connect_to_rabbitmq(host, max_retries=5, retry_delay=5):
    retries = 0
    while retries < max_retries:
        try:
            return pika.BlockingConnection(pika.ConnectionParameters(host=host))
        except pika.exceptions.AMQPConnectionError:
            retries += 1
            time.sleep(retry_delay)
    raise Exception("Failed to connect to RabbitMQ after multiple attempts")

def start_consuming(app):
    rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
    rabbitmq_exchange = 'domain_events'
    queue_name = 'dns_service_queue'

    with app.app_context():
        try:
            connection = connect_to_rabbitmq(rabbitmq_host)
            channel = connection.channel()

            channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='fanout', durable=True)
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=rabbitmq_exchange, queue=queue_name)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            app.logger.info(f'DNS service waiting for messages on queue: {queue_name}')
            
            channel.start_consuming()
        except Exception as e:
            app.logger.error(f"Error in RabbitMQ consumer: {str(e)}")
        finally:
            if connection and not connection.is_closed:
                connection.close()

def init_rabbitmq_consumer(app):
    if not hasattr(app, 'rabbitmq_consumer_thread'):
        import threading
        app.rabbitmq_consumer_thread = threading.Thread(target=start_consuming, args=(app,))
        app.rabbitmq_consumer_thread.daemon = True
        app.rabbitmq_consumer_thread.start()
