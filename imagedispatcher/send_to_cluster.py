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

from retrying import retry
import requests
import os

CLUSTER_HOST = os.environ['CLUSTER_HOST']


@retry(stop_max_attempt_number=5, wait_fixed=45000)
def perform_inference(service, image_data):
    """
    Calls the cluster endpoint and retries on a bad status.
    It retries a maximum of 5 times with a fixed delay of 45 seconds
    """
    # Perform inference
    result = requests.post(
        f'{CLUSTER_HOST}/api/v1/service/{service}/score',
        data=image_data
    )

    # Raise an error if the status is not good. This will trigger the retry
    result.raise_for_status()

    # Return the result if the status is good
    return result
