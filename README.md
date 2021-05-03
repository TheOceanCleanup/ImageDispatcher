# ImageDispatcher

This repo implemenets a Service Bus listener that:

- Listens to a topic on a service bus containing messages with a link to images
  on Blob Storage
- For each image in the message:
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
| CLUSTER_HOST | True | Entry of the cluster where the endpoints are located. Should include the schema (eg http://127.0.0.1) |
| TSS_URL | True | URL where the TimeSeriesStore is located |
| TSS_API_KEY | True | API Key to use when posting to the Time Series Store |
| TSS_API_SECRET | True | API Secret to use when posting to the Time Series Store |


# Copyright

Copyright (C) 2020-2021 The Ocean Cleanup™

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>