import pika
import json
import os
from flask import current_app

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_queue = 'domain_registration'

def send_message(message):
    try:
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
        current_app.logger.info(f"Message sent to RabbitMQ: {message}")
    except Exception as e:
        current_app.logger.error(f"Failed to send message to RabbitMQ: {str(e)}")
        raise
