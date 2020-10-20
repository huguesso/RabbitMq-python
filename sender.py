try:
    import pika
except Exception as e:
    print("Some Modules are missing {}".format(e))


class MetaClass(type):
    _instance = {}

    def __call__(cls, *args, **kwargs):
        """ Singleton design pattern  """
        """ if instance already exist dont create one """

        if cls not in cls._instance:
            cls._instance[cls] = super(
                MetaClass, cls).__call__(*args, **kwargs)
            return cls._instance[cls]


class RabbitmqConfiguration(metaclass=MetaClass):

    def __init__(self, queue="hello", host='localhost', routingKey='hello', exchange=''):
        """ Configuration Rabbitmq server  """
        self.queue = queue
        self.host = host
        self.routingKey = routingKey
        self.exchange = exchange


class RabbitMq():

    __slots__ = ["server", "_channel", "_connection"]

    def __init__(self, server):
        """ 
        :param server Objet rabbitmq config class RabbitmqConfiguration
        """

        self.server = server
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)

    def __enter__(self):
        print("__enter__")
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__")
        self._connection.close()

    def publish(self, payload={}):
        """
        :param payload JSON payload
        :return None
        """
        self._channel.basic_publish(
            exchange=self.server.exchange, routing_key=self.server.routingKey, body=str(payload))
        print("published Message {}".format(payload))


if __name__ == "__main__":
    server = RabbitmqConfiguration(
        queue="hello", host='localhost', routingKey='hello', exchange='')

    with RabbitMq(server) as rabbitmq:
        rabbitmq.publish(payload={"data": 22})
