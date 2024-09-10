import pika
import json
import os
from flask import current_app

class RabbitMQProducer:
    def __init__(self):
        self.rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
        self.queue_name = 'notification_queue'

    def send_message(self, action, data):
        try:
            connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.rabbitmq_host))
            channel = connection.channel()

            channel.queue_declare(queue=self.queue_name, durable=True)
            
            message = {
                "action": action,
                "data": data
            }
            
            channel.basic_publish(
                exchange='',
                routing_key=self.queue_name,
                body=json.dumps(message),
                properties=pika.BasicProperties(delivery_mode=2)
            )

            connection.close()
            current_app.logger.info(f"Message sent to RabbitMQ queue: {message}")
        except Exception as e:
            current_app.logger.error(f"Failed to send message to RabbitMQ: {str(e)}")
            raise

# TODO: DO not make this global
producer = RabbitMQProducer()

def send_notification_message(action, data):
    producer.send_message(action, data)
