#!/usr/bin/env python
import datetime
import json
import time
import pika

def send_message(message):
    application_broker_queue_name = 'ApplicationBroker'
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        virtual_host='/',
        credentials=pika.credentials.PlainCredentials(
            username='Manager',
            password='Qwerty123!'
        )))
    channel = connection.channel()
    timestamp = time.time()
    now = datetime.datetime.now()
    expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())
    headers = {  # example how headers can be used
        'hello': 'world',
        'created': int(timestamp)
    }
    data = {  # example hot to transfer objects rather than string using json.dumps and json.loads
        'keyword': message,
        'domain': message,
        'created': int(timestamp),
        'expire': expire
    }
    channel.basic_publish(
        exchange='',
        routing_key = application_broker_queue_name,
        body = 'hello',
        # body=json.dumps(data),  # must be string
        properties = pika.BasicProperties(
            delivery_mode=2,  # makes persistent job
            priority=0,  # default priority
            timestamp=timestamp,  # timestamp of job creation
            expiration=str(expire),  # job expiration (milliseconds from now), must be string, handled by rabbitmq
            headers=headers
        ))

if __name__ == '__main__':
    send_message('Hello!')
