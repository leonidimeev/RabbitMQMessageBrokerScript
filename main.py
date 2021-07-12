#!/usr/bin/env python
import datetime
import json
import time
import pika
import uuid
import ApplicationMasterServiceTests.application as application

class Message:
    def __init__(self, destinationAddress, headers, messageType, message):
        self.DestinationAddress = destinationAddress
        self.Headers = headers
        self.MessageType = messageType
        self.Message = message

def send_message(message):
    application_broker_queue_name = 'ApplicationBroker'
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='localhost',
        virtual_host='/',
        credentials=pika.credentials.PlainCredentials(
            username='Secret',
            password='Secret'
        )))
    channel = connection.channel()
    timestamp = time.time()
    now = datetime.datetime.now()
    expire = 1000 * int((now.replace(hour=23, minute=59, second=59, microsecond=999999) - now).total_seconds())
    headers = {
        'created': int(timestamp)
    }
    channel.basic_publish(
        exchange='',
        routing_key = application_broker_queue_name,
        body = message,
        properties = pika.BasicProperties(
            delivery_mode = 2,  # makes persistent job
            priority = 0,  # default priority
            timestamp = timestamp,  # timestamp of job creation
            expiration = str(expire),  # job expiration (milliseconds from now), must be string, handled by rabbitmq
            headers = headers
        ))

if __name__ == '__main__':
    with open('C:\Users\user\Desktop\scripts\RabbitMQMessageBrokerScript\ApplicationMasterServiceTests\Application.json', 'r') as f:
        data = f.read()
    body = json.dumps(data)
    application = application.Application(
        applicationId = uuid.uuid4(),
        affectedFields = ['all'],
        applicationChemaVersion = '0.1.0',
        completedTreatments = 'some treatments',
        applicationPatch = '{\n"body" : "message"\n}'
    )
    message = Message('rabbitmq://localhost/ApplicationBroker', '', '', application)
    # print(message.toJSON())
    # send_message(message.toJSON())

    send_message(application.toJSON())
