#!/usr/bin/env python3

# Hello! I'm a stupid little script to do something that connects to
# the rabbitMQ service.

import pika

# This is for a demo only! For an actual production thing, please
# export these to the environment.
credentials = pika.PlainCredentials('fluxuser', 'fluxrabbit')
parameters = pika.ConnectionParameters('rabbit',
                                       5672,
                                       '/',
                                       credentials)
connection = pika.BlockingConnection(parameters)
channel = connection.channel()

channel.queue_declare(queue='hello')
channel.basic_publish(exchange='',
                      routing_key='hello',
                      body='Hello World!')
print("👋️ Sent 'Hello World!'")
connection.close()


