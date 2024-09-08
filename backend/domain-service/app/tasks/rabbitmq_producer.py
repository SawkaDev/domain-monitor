import pika
import json
import os
from flask import current_app

rabbitmq_host = os.environ.get('RABBITMQ_HOST', 'localhost')
rabbitmq_exchange = 'domain_events'

def send_message(message):
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host=rabbitmq_host))
        channel = connection.channel()

        channel.exchange_declare(exchange=rabbitmq_exchange, exchange_type='fanout', durable=True)
        channel.basic_publish(
            exchange=rabbitmq_exchange,
            routing_key='',
            body=json.dumps(message),
            properties=pika.BasicProperties(delivery_mode=2)
        )

        connection.close()
        current_app.logger.info(f"Message sent to RabbitMQ exchange: {message}")
    except Exception as e:
        current_app.logger.error(f"Failed to send message to RabbitMQ: {str(e)}")
        raise
