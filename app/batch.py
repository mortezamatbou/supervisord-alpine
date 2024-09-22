import os
import pika

rabbit_username = os.environ.get('RABBITMQ_USER')
rabbit_password = os.environ.get('RABBITMQ_PASSWORD')
rabbit_port = os.environ.get('RABBITMQ_PORT')
rabbit_host = os.environ.get('RABBITMQ_HOST')

connection = pika.BlockingConnection(
    pika.URLParameters(f"amqp://{rabbit_username}:{rabbit_password}@{rabbit_host}:{rabbit_port}/")
)
channel = connection.channel()
channel.queue_declare(queue="test", durable=True)


while True:
    txt = input("Enter your qoute: ")
    txt = txt.strip()

    if txt.lower() == 'exit':
        break

    try:
        channel.basic_publish(exchange="", routing_key="test", body=txt, properties=pika.BasicProperties(
            delivery_mode=pika.DeliveryMode.Persistent
        ))
    except Exception as e:
        print(repr(e))

connection.close()

