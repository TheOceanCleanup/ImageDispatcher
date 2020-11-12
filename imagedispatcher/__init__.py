from .utils import create_logger, MessageBusWrapper, Parser, StorageClient
from .model_select import select_service
import os
import json
import requests

logger = create_logger(os.getenv('LOGLEVEL', 'DEBUG'), __name__)


def parse_messages():

    SERV_BUS_CONNECTION_STRING = os.environ['SB_CONNECTION']
    TOPIC_NAME = os.environ['SB_TOPIC_NAME']
    SUBSCRIPTION_NAME = os.environ['SB_SUBSCRIPTION_NAME']
    STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    STORAGE_CONTAINER_NAME = os.environ['AZURE_STORAGE_CONTAINER_NAME']
    # CLUSTER_IP = os.environ['CLUSTER_IP']
    # TSS_URL = os.environ['TSS_URL']
    # TSS_API_KEY = os.environ['TSS_API_KEY']
    # TSS_API_SECRET = os.environ['TSS_API_SECRET']

    message_bus_client = MessageBusWrapper(SERV_BUS_CONNECTION_STRING, SUBSCRIPTION_NAME, TOPIC_NAME)
    storage_client = StorageClient(STORAGE_CONNECTION_STRING, STORAGE_CONTAINER_NAME)

    print("Listening")
    for message in message_bus_client.get_messages():
        try:
            item = Parser.parse(message.body())
            print(item)
            message.success()

            # TODO implement operations

            for image in item['image_paths']:
                try:
                    image_data = storage_client.download(image['path'])
                except Exception as e:
                    msg = "Failed to download image on " + image['path']
                    print(e)
                    logger.error(msg)
                    continue

                print(len(image_data))

                # Determine Endpoint
                service = select_service(item.payload)

                # Send image to Endpoint
                r = requests.post(
                    f'http://{CLUSTER_IP}/api/v1/service/{service}/score'
                    data=image_data
                )
                if r.status_code == 200:
                    result = r.data
                else:
                    msg = "Failed to perform inference"
                    logger.error(msg)
                    message.failure(msg)
                    continue

                # # Post result back to TimeSeriesStore
                # headers = {
                #     'Authentication-Key': API_KEY,
                #     'Authentication-Secret': API_SECRET
                # }

                # # TODO: Fill in
                # json_payload = {
                #     'device_serial_number': '0kRM0jpD40P2pCqRdnwx',
                #     'timestamp': '2020-04-07T15:15:52+00:00',
                #     'payload': {'some': 'structure'},
                #     'type': 'autonaut',
                #     'revision': 'v1'
                # }

                # r = requests.post(url, json=json_payload, headers=headers)
                # if r.status_code == 200:
                    # message.success()
                # else:
                #     msg = "Failed to submit result to TimeSeriesStore"
                #     logger.error(msg)
                #     message.failure(msg)
                #     continue

        except Exception as e:
            logger.error(e)
            # message.failure(e)
