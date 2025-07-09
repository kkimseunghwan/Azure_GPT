# 로컬에서 테스트 시, 포트 겹칠 수 있음
#       =>> func host start --port 7072

import azure.functions as func
import logging
from openai import OpenAI
import os
import json
from util.servicebus import servicebus_client

app = func.FunctionApp()
client = OpenAI()


# queue_name: 어떤 큐에 메세지가 들어왔을 때, 아래의 함수를 실행시킬지
@app.service_bus_queue_trigger(arg_name="msg", queue_name="process-request-queue", connection="SERVICEBUS_CONNECTION_URL") 
async def process_request(msg: func.ServiceBusMessage):
    # json.loads : 문자열이 JSON 형식으로 바뀜
    message = json.loads(msg.get_body().decode('utf-8'))

    logging.info('Python ServiceBus Queue trigger processed a message: %s', msg.get_body().decode('utf-8'))

    completion = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "질문에 대해서 한국어로 답변해 주세요. 질문이 영어로 되어 있더라도 한국어로 답변해 주세요."
            },
            {
                "role": "user",
                "content": message['content']
            } 
        ]
    )

    answer_data = {
        "channel_id": message['channel_id'],
        "content": completion.choices[0].message.content,
        "type": "answer"
    }

    await servicebus_client.send_message(answer_data, queue_name="process-response-queue")

    logging.info(completion.choices[0].message.content)

