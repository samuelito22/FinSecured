import pika
import json
from sentence_transformers import SentenceTransformer
from sentence_transformers.quantization import quantize_embeddings

def callback(ch, method, properties, body):
    input_data = json.loads(body)
    texts = input_data['texts']

    model = SentenceTransformer("mixedbread-ai/mxbai-embed-large-v1")
    embeddings = model.encode(texts)
    binary_embeddings = quantize_embeddings(embeddings, precision="binary")

    result = {"binary_embeddings": binary_embeddings.tolist()}
    print(json.dumps(result))

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='embeddings_queue')

channel.basic_consume(queue='embeddings_queue', on_message_callback=callback, auto_ack=True)

print('Waiting for messages. To exit press CTRL+C')
channel.start_consuming()
