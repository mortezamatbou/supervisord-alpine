import os
import pika

rabbit_username = os.environ.get('RABBITMQ_USER')
rabbit_password = os.environ.get('RABBITMQ_PASSWORD')
rabbit_port = os.environ.get('RABBITMQ_PORT')
rabbit_host = os.environ.get('RABBITMQ_HOST')

def main():
    connection = pika.BlockingConnection(
        pika.URLParameters(f"amqp://{rabbit_username}:{rabbit_password}@{rabbit_host}:{rabbit_port}/"),
    )
    channel = connection.channel()
    channel.queue_declare(queue="test", durable=True)

    def callback(ch, method, properties, body):
        print(f"Received : {body.decode()}")
        ch.basic_ack(delivery_tag=method.delivery_tag)
        # ch.basic_nack(delivery_tag=method.delivery_tag)


    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(
        queue="test",
        on_message_callback=callback,
        auto_ack=False,
    )

    # print(" [*] Waiting for messages. To exit press CTRL+C")
    channel.start_consuming()


if __name__ == "__main__":
    main()
