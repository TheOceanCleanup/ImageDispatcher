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
