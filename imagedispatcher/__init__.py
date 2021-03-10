from .utils import create_logger, MessageBusWrapper, Parser, StorageClient, Sentry
from .model_select import select_service
from .send_to_cluster import perform_inference
import os
import requests
import datetime

logger = create_logger(os.getenv('LOGLEVEL', 'DEBUG'), __name__)


def parse_messages():

    # Configure Sentry
    sentry = Sentry("https://abeb55d9752a49bbbd99e5a92d33d107@o486030.ingest.sentry.io/5561411")
    sentry.add_sensitive_value(os.environ['SB_CONNECTION'])
    sentry.add_sensitive_value(os.environ['AZURE_STORAGE_CONNECTION_STRING'])
    sentry.add_sensitive_value(os.environ['TSS_API_SECRET'])

    SERV_BUS_CONNECTION_STRING = os.environ['SB_CONNECTION']
    TOPIC_NAME = os.environ['SB_TOPIC_NAME']
    SUBSCRIPTION_NAME = os.environ['SB_SUBSCRIPTION_NAME']
    STORAGE_CONNECTION_STRING = os.environ['AZURE_STORAGE_CONNECTION_STRING']
    STORAGE_CONTAINER_NAME = os.environ['AZURE_STORAGE_CONTAINER_NAME']
    TSS_URL = os.environ['TSS_URL']
    TSS_API_KEY = os.environ['TSS_API_KEY']
    TSS_API_SECRET = os.environ['TSS_API_SECRET']

    message_bus_client = MessageBusWrapper(
        SERV_BUS_CONNECTION_STRING, SUBSCRIPTION_NAME, TOPIC_NAME)
    storage_client = StorageClient(
        STORAGE_CONNECTION_STRING, STORAGE_CONTAINER_NAME)

    for message in message_bus_client.get_messages():
        try:
            # Forget about previous message
            sentry.clear_breadcrumbs()

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
                try:
                    r = perform_inference(service, image_data)
                    result = r.json()
                except Exception as e:
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
                        'message_id': item['id'],
                        'image_path': image['path'],
                        'model_used': {
                            'service': service,
                            'model': model,
                            'version': version
                        },
                        'bounding_boxes': result
                    },
                    'type': 'ai-result',
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
            message.failure(e)
