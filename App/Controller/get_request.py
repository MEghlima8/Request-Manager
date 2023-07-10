import pika
from App.Controller.process import process

def main():
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()

    # It will create a queue if doesn't exist. To be sure there is queue
    channel.queue_declare(queue='requests')

    # Whenever we receive a message, this callback function is called
    def callback(ch, method, properties, body):
        print(".................. Received ..................")
        
        proc_res = process(int(body.decode()))
        return proc_res

    channel.basic_consume(queue='requests', on_message_callback=callback, auto_ack=True)

    channel.start_consuming()