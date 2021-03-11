import logging, json, base64, traceback, random, time
from typing import Dict
from datetime import datetime
from azure.servicebus import ServiceBusClient
from azure.common import AzureMissingResourceHttpError

logger = logging.getLogger(__name__)


def create_logger(loglevel: str, log_name: str):
    logger = logging.getLogger(log_name)
    if not logger.handlers:
        logger.setLevel(loglevel)
        ch = logging.StreamHandler()
        log_format = logging.Formatter("%(asctime)s [%(filename)s:%(lineno)s - %(funcName)s() ] %(message)s")
        ch.setFormatter(log_format)
        logger.addHandler(ch)
    return logger


class MessageBusWrapper:
    def __init__(self, serv_bus_cs: str, subscription_name: str, topic_name: str):
        self.serv_bus_cs = serv_bus_cs
        self.subscription_name = subscription_name
        self.topic_name = topic_name

    def get_messages(self):
        """
        Wait and yield messages from the service bus
        """
        while True:
            try:
                self._set_clients()
                with self.topic_client.get_receiver() as messages:
                    for message in messages:  # This waits for the next message
                        yield MessageWrapper(message)
            except Exception as e:
                logger.error('Something went wrong while getting a new message ')
                logger.exception(e)
                time.sleep(random.randint(1, 60))

    def _set_clients(self):
        self.servicebus_client = ServiceBusClient.from_connection_string(conn_str=self.serv_bus_cs)
        try:
            # needs to use self variables but somehow topic_client gets wrongly initiated and doesn't work
            self.topic_client = self.servicebus_client.get_subscription(topic_name=self.topic_name,
                                                                        subscription_name=self.subscription_name)
        except AzureMissingResourceHttpError as _:
            logger.debug('Subscription {} for topic {} does not exist, creating it'.format(self.subscription_name,
                                                                                           self.topic_name))
            self.servicebus_client.create_subscription(self.topic_name, self.subscription_name)
            self.topic_client = self.servicebus_client.get_subscription(topic_name=self.topic_name,
                                                                        subscription_name=self.subscription_name)


class MessageWrapper:
    def __init__(self, raw_message):
        self.raw_message = raw_message

    def body(self):
        """
        Deserialize raw message from the queue into a dictionary
        :return: dictionary containing the deserialized message
        """
        message_string = "".join(el.decode("UTF-8") for el in self.raw_message.body)
        # Load string to JSON
        message: Dict = json.loads(message_string)
        message['timestamp'] = datetime.strptime(message['timestamp'], '%Y%m%dT%H%M')
        if message['binary_payload'] is not None:
            message['binary_payload'] = base64.b64decode(message['binary_payload'])
        return message

    def success(self):
        """
        Mark message as complete
        :return: None
        """
        try:
            self.raw_message.complete()
        except Exception as e:
            logger.error('An error occured while marking message as complete')
            logger.exception(e)

    def failure(self, e):
        """

        :param e: Exception why the message failed
        :return:
        """
        try:
            logger.info('Failed to handle message:')
            logger.info("".join(el.decode("UTF-8") for el in self.raw_message.body))
            logger.exception(e)
            self.raw_message.dead_letter(traceback.format_exc())
        except Exception as e:
            logger.error('An error occured while marking message as failed')
            logger.exception(e)
