#!/usr/bin/env python
import pika, sys, os, json
from worker import response_function

CREDENTIALS = pika.PlainCredentials('test_admin', 'admin1234')
PARAMETERS = pika.ConnectionParameters('210.183.178.47',
                                       25672,
                                       '/',
                                       credentials=CREDENTIALS)

def main():
    with pika.BlockingConnection(parameters=PARAMETERS) as connection:
        with connection.channel() as channel:
            channel.queue_declare(queue='rpc_queue')
            channel.queue_declare(queue='rpc_queue_return')

            def callback(ch, method, props, body):
                print(f" [x] Received")
                print(f" body: {body}")

                response = response_function(body)

                ch.basic_publish(exchange='',
                    routing_key=props.reply_to,
                    properties = pika.BasicProperties(correlation_id = props.correlation_id),
                    body=str(response))


            channel.basic_consume(queue='rpc_queue', on_message_callback=callback, auto_ack=True)

            print(' [*] Waiting for messages. To exit press CTRL+C')
            channel.start_consuming()

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('Interrupted')
        try:
            sys.exit(0)
        except SystemExit:
            os._exit(0)