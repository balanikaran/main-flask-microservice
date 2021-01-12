import pika
import json

rabbitMQ_url = 'amqps://gyjabiuq:T6BgZbtVk2_aoDzGG0tLXAu1CRRhMXea@lionfish.rmq.cloudamqp.com/gyjabiuq'
params = pika.URLParameters(rabbitMQ_url)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()


def publish(method, body):
    properties = pika.BasicProperties(method)
    channel.basic_publish(exchange='', routing_key='admin', body=json.dumps(body), properties=properties)
