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

from azure.storage.blob import BlockBlobService
from retrying import retry


class StorageClient:
    def __init__(self, connection_string, container):
        self.block_blob_service = BlockBlobService(
            connection_string=connection_string
        )
        self.container = container


    @retry(stop_max_attempt_number=5, wait_exponential_multiplier=1000,
        wait_exponential_max=10000)
    def download(self, path):
        return self.block_blob_service.get_blob_to_bytes(
            self.container,
            path
        ).content
