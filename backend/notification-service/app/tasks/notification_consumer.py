import pika
import json
import os
import threading
import time
from flask import current_app

class RabbitMQConsumer:
    def __init__(self, app):
        self.app = app
        self.rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.queue_name = 'notification_queue'

    def callback(self, ch, method, properties, body):
        with self.app.app_context():
            try:
                message = json.loads(body)
                action = message.get('action')
                data = message.get('data')

                # This is where you normally would use an email API to build and send a message to all users who subscribed for updates
                # For the purpose of this exercise, we will just log the message to the console
                # Normally you could querty the notification database to get the list of users to send the message to
                if action == 'whois_notification':
                    current_app.logger.info(f"Sending WHOIS notification for domain: {data}")
                elif action == 'dns_notification':
                    current_app.logger.info(f"Sending DNS notification for domain: {data}")
                else:
                    current_app.logger.warning(f"Unknown action received: {action}")
            except json.JSONDecodeError:
                current_app.logger.error("Received invalid JSON message")
            except Exception as e:
                current_app.logger.error(f"Error processing message: {str(e)}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def connect_to_rabbitmq(self, max_retries=5, retry_delay=5):
        retries = 0
        while retries < max_retries:
            try:
                return pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
            except pika.exceptions.AMQPConnectionError:
                retries += 1
                time.sleep(retry_delay)
        raise Exception("Failed to connect to RabbitMQ after multiple attempts")

    def start_consuming(self):
        with self.app.app_context():
            try:
                connection = self.connect_to_rabbitmq()
                channel = connection.channel()

                channel.queue_declare(queue=self.queue_name, durable=True)
                channel.basic_qos(prefetch_count=1)
                channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
                
                self.app.logger.info(f'Notification service waiting for messages on queue: {self.queue_name}')
                channel.start_consuming()
            except Exception as e:
                self.app.logger.error(f"Error in RabbitMQ consumer: {str(e)}")
            finally:
                if connection and not connection.is_closed:
                    connection.close()

def init_rabbitmq_consumer(app):
    if not hasattr(app, 'rabbitmq_consumer_thread'):
        consumer = RabbitMQConsumer(app)
        app.rabbitmq_consumer_thread = threading.Thread(target=consumer.start_consuming)
        app.rabbitmq_consumer_thread.daemon = True
        app.rabbitmq_consumer_thread.start()
