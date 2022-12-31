from app.functions.env import EnvVars
import pika
from app.signer import UrlSigner

from app.callbacks import *

env_vars = EnvVars()  # Load in environment variables
signer = UrlSigner(env_vars.bucket_region, env_vars.bucket_endpoint, env_vars.bucket_key_id, env_vars.bucket_access_key)
# Message Broker--------
connection = pika.BlockingConnection(pika.connection.URLParameters(env_vars.mq_uri))  # Connect to message broker
channel = connection.channel()  # creates connection channel
channel.queue_declare(queue="film-url")  # Declare Queue
channel.basic_consume(queue="film-url", on_message_callback=lambda ch, method, properties, body:
                      url_sign_callback(ch, method, properties, body, signer))
# Start application consumer
channel.start_consuming()
connection.close()
