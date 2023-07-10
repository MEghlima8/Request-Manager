import pika

def send(val):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='requests')

    channel.basic_publish(exchange='', routing_key='requests', body=val)

    connection.close()
    
    return 'true'