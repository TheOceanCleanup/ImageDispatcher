# ImageDispatcher - ServiceBus listeners that calls Image Recognition model to detect plastic objects in queued images
# Copyright (C) 2020-2021 The Ocean Cleanup™
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

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
