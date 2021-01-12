import pika
import json
from main import Product, db

rabbitMQ_url = 'amqps://gyjabiuq:T6BgZbtVk2_aoDzGG0tLXAu1CRRhMXea@lionfish.rmq.cloudamqp.com/gyjabiuq'

params = pika.URLParameters(url=rabbitMQ_url)

connection = pika.BlockingConnection(parameters=params)

channel = connection.channel()

channel.queue_declare(queue='main')


def callback(channel_name, method, properties, body):
    print("Received in MAIN - FLASK APP")
    data = json.loads(body)
    print("Data: ", data)

    if properties.content_type == 'product_created':
        product = Product(id=data['id'], title=data['title'], image=data['image'])
        db.session.add(product)
        db.session.commit()
        print("product created")

    elif properties.content_type == 'product_updated':
        product = Product.query.get(data['id'])
        product.title = data['title']
        product.image = data['image']
        db.session.commit()
        print("product updated")

    elif properties.content_type == 'product_deleted':
        product = Product.query.get(data)
        db.session.delete(product)
        db.session.commit()
        print("product deleted")


channel.basic_consume(queue='main', on_message_callback=callback, auto_ack=True)

print("Started Consuming... [consumer in main-flask-microservice]")

channel.start_consuming()

# channel.close()
