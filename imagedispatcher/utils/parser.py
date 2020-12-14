from typing import Dict
import logging

logger = logging.getLogger(__name__)


class Parser:
    @staticmethod
    def parse(message: Dict) -> Dict:
        revision = message.get('revision', None)
        if revision in 'v1':
            return Parser._parse_v1(message)
        else:
            raise Exception('Unknown version encountered {}, no known parser'.format(revision))

    @staticmethod
    def _parse_v1(message: Dict) -> Dict:
        payload = message['payload']

        parsed_payload = dict()

        images = []
        for k, v in payload['attachments'].items():
            images.append({'filename': k, 'path': v['path']})

        parsed_payload['device_serial_number'] = message['device_serial_number']
        parsed_payload['timestamp'] = payload['original_timestamp']
        parsed_payload['payload'] = payload
        parsed_payload['image_paths'] = images
        parsed_payload['id'] = payload['message_id']

        logger.debug("Parsed message: {}".format(parsed_payload))

        return parsed_payload
