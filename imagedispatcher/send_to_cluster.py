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
