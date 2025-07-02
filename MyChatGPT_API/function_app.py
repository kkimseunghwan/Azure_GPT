# Python Version : 3.11.9
from typing import Union
from fastapi import FastAPI
from dto.question import QuestionRequest
from azure.messaging.webpubsubservice.aio import WebPubSubServiceClient
from azure.core.credentials import AzureKeyCredential
from fastapi.middleware.cors import CORSMiddleware
import os
import azure.functions as func
import uuid

# MyChatGPT API
# Azure Web PubSub Service Client 설정
pubsub_client = WebPubSubServiceClient(endpoint=os.environ['PUBSUB_CONNECTION_URL'], 
                                       hub=os.environ['PUBSUB_HUB'], 
                                       credential=AzureKeyCredential(os.environ['PUBSUB_KEY']))

fast_app = FastAPI()
fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app = func.AsgiFunctionApp(app=fast_app , http_auth_level=func.AuthLevel.ANONYMOUS)

# 질문 API
@fast_app.post("/question")
async def send_question(request: QuestionRequest):
    return request

# 랜덤한 채널 아이디 생성
@fast_app.get("/channel-id")
async def get_channel_id():
    return {"channel_id": str(uuid.uuid4())}
    # TODO: 혹시 모를 상황을 대비해, DB에 중복된 채널값이 있으면 재생성 필요



# Pubsub 토큰을 발급하는 API
@fast_app.get("/pubsub/token")
async def get_pubsub_token(channel_id: str):
    try:
        return await pubsub_client.get_client_access_token(
            groups = [ channel_id ],
            minutes_to_expire = 5,
            roles = [ 'webpubsub.joinLeaveGroup.' + channel_id ] 
        )
    except Exception as e:
        return {"error": str(e)}

