from motor.motor_asyncio import AsyncIOMotorClient
import os

db_client = AsyncIOMotorClient(os.environ['DB_CONNECTION_URL'])
db = db_client['myGPT']

# messages 컬렉션의 channel_id 필드에 인덱스 생성
db.messages.create_index("channel_id")