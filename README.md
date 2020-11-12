# ImageDispatcher

This repo implemenets a Service Bus listener that:

- Listens to a topic on a service bus containing messages with a link to images
  on Blob Storage
- Downloads this image
- Chooses an Azure ML endpoint based on metadata with the image
- Offers the image to this Azure ML endpoint, where object detection is applied
- Submits the result of the object detection to the TimeSeriesStore

# Configuration

The following environment variables can/need to be provided

| Variable | Required | Description |
| --- | --- | --- |
| AZURE_STORAGE_CONNECTION_STRING | True | Connection string for the blob storage account |
| AZURE_STORAGE_CONTAINER_NAME | True | Container where the images are stored |
| SB_CONNECTION | True | Connection string to the Service Bus |
| SB_TOPIC_NAME | True | Topic on the Service Bus to listen to |
| SB_SUBSCRIPTION_NAME | True | Subscription on the Service Bus to use |
| CLUSTER_IP | True | Entry of the cluster where the endpoints are located |
| TSS_URL | True | URL where the TimeSeriesStore is located |
| TSS_API_KEY | True | API Key to use when posting to the Time Series Store |
| TSS_API_SECRET | True | API Secret to use when posting to the Time Series Store |


