from typing import Dict
from datetime import datetime, timedelta
import logging
import msgpack

logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def parse(message: Dict) -> list:
        revision = message.get('revision', None)
        if revision == 'v1':
            return Parser._parse_v1(message)
        else:
            raise Exception('Unknown version encountered {}, no known parser'.format(revision))

    @staticmethod
    def _parse_v1(message: Dict) -> list:
        payload = message['payload']

        parsed_payload = dict()

        images = []
        for k, v in message['attachments'].items():
            images.append({'filename': k, 'path': v['path']})

        parsed_payload['device_serial_number'] = message['device_serial_number']
        parsed_payload['timestamp'] = message['timestamp']
        parsed_payload['payload'] = payload
        parsed_payload['image_paths'] = images

        logger.debug("Parsed message: {}".format(parsed_payload))

        return parsed_payload
