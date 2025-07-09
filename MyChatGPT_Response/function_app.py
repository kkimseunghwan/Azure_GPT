
import azure.functions as func
from util.pubsub import pubsub_client
from util.database import db
import logging
import json

app = func.FunctionApp()

@app.service_bus_queue_trigger(arg_name="msg", queue_name="process-response-queue", connection="SERVICEBUS_CONNECTION_URL") 
async def process_response_function(msg: func.ServiceBusMessage):
    response = json.loads(msg.get_body().decode('utf-8'))

    await db.messages.insert_one(response)

    response['_id'] = str(response['_id'])  # MongoDB ObjectId를 문자열로 변환
    await pubsub_client.send_to_group(group=response['channel_id'], message=response) # message는 JSON 형식으로 전달 가능

    logging.info('Python ServiceBus Queue trigger processed a message: %s', msg.get_body().decode('utf-8'))
