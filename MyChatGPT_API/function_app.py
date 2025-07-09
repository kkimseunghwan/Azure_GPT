# Python Version : 3.11.9
from typing import Union
from fastapi import FastAPI
from dto.question import QuestionRequest
from fastapi.middleware.cors import CORSMiddleware
import azure.functions as func
import uuid

# 싱글톤 패턴으로 Azure 클라이언트 생성
from util.servicebus import servicebus_client
from util.pubsub import pubsub_client
from util.database import db


fast_app = FastAPI()
fast_app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)
app = func.AsgiFunctionApp(app=fast_app , http_auth_level=func.AuthLevel.ANONYMOUS)

# 질문 API
# 메세지를 보내는 API
@fast_app.post("/question")
async def send_question(request: QuestionRequest):

    # 메세지 전달하기 위한 Json 형식 데이터 생성
    # DB에 답변과 질문 형식을 구분해야하기 때문에 "type" 필드를 추가
    question_json_data = {
        "channel_id": request.channel_id,
        "content": request.content,
        "type": "question"
    }

    # 메세지 데이터를 DB에 저장 
    result = await db.messages.insert_one(question_json_data)

    # !오류 주의
    # question_json_data값을 DB에 insert 할 시, 내부에 _id 필드가 자동으로 생성됨
    # 이 _id 필드는 MongoDB에서 자동으로 생성되는 ObjectId 타입이기 때문에
    # 이를 str로 변환하지 않으면, JSON 직렬화 과정에서 오류가 발생할 수 있음
    question_json_data['_id'] = str(question_json_data['_id']) # str로 변환

    # 큐에 메세지 전달
    await servicebus_client.send_message(question_json_data, queue_name="process-request-queue")

    # result.inserted_id: 기본적으로 str이 아님
    return str(result.inserted_id)

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

