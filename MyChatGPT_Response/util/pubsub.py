from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
import os

# MyChatGPT API
# Azure Web PubSub Service Client 설정
pubsub_client = WebPubSubServiceClient(endpoint=os.environ['PUBSUB_CONNECTION_URL'], 
                                       hub=os.environ['PUBSUB_HUB'], 
                                       credential=AzureKeyCredential(os.environ['PUBSUB_KEY']))


