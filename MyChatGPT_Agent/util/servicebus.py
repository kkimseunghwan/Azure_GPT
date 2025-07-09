from azure.servicebus.aio import ServiceBusClient
from azure.servicebus import ServiceBusMessage
import json
import os

class ServiceBus():
    client = None

    def __init__(self):
        self.client = ServiceBusClient.from_connection_string(conn_str=os.environ['SERVICEBUS_CONNECTION_URL'], logging_enable=True)

    async def send_message(self, data, queue_name="process-response-queue"):
        # 큐에 메세지 전달
        async with self.client:
            sender = self.client.get_queue_sender(queue_name=queue_name)

            # sender 를 열기 (얘도 with 문법 사용)
            async with sender:
                message = ServiceBusMessage(json.dumps(data))        
                await sender.send_messages(message)


servicebus_client = ServiceBus()