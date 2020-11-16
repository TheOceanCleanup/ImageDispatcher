from .utils import create_logger, MessageBusWrapper, Parser, StorageClient
from .model_select import select_service
import os
import json
import requests
import datetime

logger = create_logger(os.getenv('LOGLEVEL', 'DEBUG'), __name__)


def parse_messages():

    SERV_BUS_CONNECTION_STRING = os.environ['SB_CONNECTION']
    TOPIC_NAME = os.environ['SB_TOPIC_NAME']
    SUBSCRIPTION_NAME = os.environ['SB_SUBSCRIPTION_NAME']
    STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    STORAGE_CONTAINER_NAME = os.environ['AZURE_STORAGE_CONTAINER_NAME']
    CLUSTER_HOST = os.environ['CLUSTER_HOST']
    TSS_URL = os.environ['TSS_URL']
    TSS_API_KEY = os.environ['TSS_API_KEY']
    TSS_API_SECRET = os.environ['TSS_API_SECRET']

    message_bus_client = MessageBusWrapper(
        SERV_BUS_CONNECTION_STRING, SUBSCRIPTION_NAME, TOPIC_NAME)
    storage_client = StorageClient(
        STORAGE_CONNECTION_STRING, STORAGE_CONTAINER_NAME)

    print("Listening")
    for message in message_bus_client.get_messages():
        try:
            item = Parser.parse(message.body())

            for image in item['image_paths']:
                try:
                    image_data = storage_client.download(image['path'])
                except Exception as e:
                    msg = "Failed to download image on " + image['path']
                    logger.error(msg)
                    continue

                # Determine Endpoint
                service, model, version = select_service(item)

                # Send image to Endpoint
                r = requests.post(
                    f'{CLUSTER_HOST}/api/v1/service/{service}/score',
                    data=image_data
                )
                if r.status_code == 200:
                    result = r.json()
                else:
                    msg = "Failed to perform inference"
                    logger.error(msg)
                    message.failure(msg)
                    continue

                # Post result back to TimeSeriesStore
                headers = {
                    'Authentication-Key': TSS_API_KEY,
                    'Authentication-Secret': TSS_API_SECRET
                }

                # Prepare message
                json_payload = {
                    'device_serial_number': item['device_serial_number'],
                    'timestamp':
                        datetime.datetime.now().strftime("%Y-%m-%dT%H:%M:%S%z"),
                    'payload': {
                        'image_path': image['path'],
                        'model_used': {
                            'service': service,
                            'model': model,
                            'version': version
                        },
                        'bouding_boxes': result
                    },
                    'type': 'bounding_boxes',
                    'revision': 'v1'
                }

                r = requests.post(TSS_URL, json=json_payload, headers=headers)
                if r.status_code == 200:
                    message.success()
                else:
                    msg = "Failed to submit result to TimeSeriesStore"
                    logger.error(msg)
                    message.failure(msg)
                    continue

        except Exception as e:
            logger.error(e)
            # message.failure(e)
