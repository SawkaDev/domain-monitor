import pika
import json
import os
import threading
from flask import current_app

class RabbitMQConsumer:
    def __init__(self, app):
        self.app = app
        self.rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.queue_name = 'notification_queue'

    def callback(self, ch, method, properties, body):
        with self.app.app_context():
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
                current_app.logger.warning(f"Unknown message type to sendtype: {mesasge_type}")

        ch.basic_ack(delivery_tag=method.delivery_tag)

    def start_consuming(self):
        with self.app.app_context():
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue_name, durable=True)
            channel.basic_qos(prefetch_count=1)
            channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback)
            
            self.app.logger.info(f'Consumer waiting for messages on queue: {self.queue_name}')
            channel.start_consuming()

def init_rabbitmq_consumer(app):
    if not hasattr(app, 'rabbitmq_consumer_thread'):
        consumer = RabbitMQConsumer(app)
        app.rabbitmq_consumer_thread = threading.Thread(target=consumer.start_consuming)
        app.rabbitmq_consumer_thread.daemon = True
        app.rabbitmq_consumer_thread.start()
