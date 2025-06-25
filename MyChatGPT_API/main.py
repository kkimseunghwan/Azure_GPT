import token
from typing import Union
from fastapi import FastAPI
from dto.question import QuestionRequest
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')
load_dotenv(dotenv_path=dotenv_path)

PUBSUB_ENDPOINT = os.environ.get('PUBSUB_ENDPOINT')
PUBSUB_HUB = os.environ.get('PUBSUB_HUB')
PUBSUB_ACCESS_KEY = os.environ.get('PUBSUB_ACCESS_KEY')

# MyChatGPT API
# Azure Web PubSub Service Client 설정
pubsub_client = WebPubSubServiceClient(endpoint=PUBSUB_ENDPOINT, hub=PUBSUB_HUB, credential=AzureKeyCredential(PUBSUB_ACCESS_KEY))

app = FastAPI()


# 질문 API
@app.post("/question")
async def send_question(request: QuestionRequest):
    return request

# Pubsub 토큰을 발급하는 API
@app.get("/pubsub/token")
async def get_pubsub_token(channel_id: str):
    try:
        return await pubsub_client.get_client_access_token(
            groups = [ channel_id ],
            minutes_to_expire = 5,
            role= [ 'webpubsub.joinLeaveGroup.' + channel_id ] 
        )
    except Exception as e:
        return {"error": str(e)}

