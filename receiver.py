try:
    import pika
    import ast
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


class RabbitmqServerConfigure(metaclass=MetaClass):

    def __init__(self, queue="hello", host='localhost'):
        """ 
        Server initialization
        :param queue 
        :param host 
        """
        self.queue = queue
        self.host = host


class RabbitmqSerever():

    def __init__(self, server):
        """ 
        :param server is objet of class RabbitmqServerConfigure
        """
        self.server = server
        self._connection = pika.BlockingConnection(
            pika.ConnectionParameters(host=self.server.host))
        self._channel = self._connection.channel()
        self._channel.queue_declare(queue=self.server.queue)
        print("Server started  Waiting for Messages")

    @staticmethod
    def callback(ch, method, properties, body):
        payload = body.decode('utf-8')
        payload = ast.literal_eval(payload)
        print(type(payload))
        print(" [x] Received %r" % payload)

    def startserver(self):
        self._channel.basic_consume(
            queue=self.server.queue, on_message_callback=RabbitmqSerever.callback, auto_ack=True)
        self._channel.start_consuming()


if __name__ == "__main__":
    server = RabbitmqServerConfigure(queue="hello", host='localhost')
    rabbitmq = RabbitmqSerever(server)
    rabbitmq.startserver()
