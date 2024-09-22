import os
import pika
from datetime import datetime

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
        txt = body.decode()
        f = open('./worker1.txt', 'a')
        d = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        f.write(f"{txt} {d}")
        f.write("\n")
        f.close()
        print("Recived: " + txt + " " + d)
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
