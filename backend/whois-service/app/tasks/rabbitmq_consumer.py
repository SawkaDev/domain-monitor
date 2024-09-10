import pika
import json
import os
import time
from flask import current_app

def callback(ch, method, properties, body):
    with current_app.app_context():
        try:
            message = json.loads(body)
            current_app.logger.info(f"WHOIS CALLBACK: Received message for domain {message.get('domain')}")

            if message['action'] == 'create_dns_records':
                domain = message.get('domain')
                domain_id = message.get('domain_id')

                if not domain or not domain_id:
                    raise ValueError("Received message without domain or domain_id")

                from app.services.whois_service import WhoisService
                success = WhoisService.create_initial_whois_record(domain, domain_id)
                if success:
                    current_app.logger.info(f"Created initial WHOIS record for {domain}")
                else:
                    current_app.logger.info(f"WHOIS record already exists for {domain}")
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
    queue_name = 'whois_service_queue'

    with app.app_context():
        try:
            connection = connect_to_rabbitmq(rabbitmq_host)
            channel = connection.channel()

            channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='fanout', durable=True)
            channel.queue_declare(queue=queue_name, durable=True)
            channel.queue_bind(exchange=rabbitmq_exchange, queue=queue_name)
            
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=queue_name, on_message_callback=callback)
            app.logger.info(f'WHOIS service waiting for messages on queue: {queue_name}')
            
            channel.start_consuming()
        except Exception as e:
            app.logger.error(f"Error in RabbitMQ consumer: {str(e)}")
        finally:
            if connection and not connection.is_closed:
                connection.close()

def init_rabbitmq_consumer(app):
    if not hasattr(app, 'whois_rabbitmq_consumer_thread'):
        import threading
        app.whois_rabbitmq_consumer_thread = threading.Thread(target=start_consuming, args=(app,))
        app.whois_rabbitmq_consumer_thread.daemon = True
        app.whois_rabbitmq_consumer_thread.start()
