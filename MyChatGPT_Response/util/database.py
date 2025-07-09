from motor.motor_asyncio import AsyncIOMotorClient
import os

db_client = AsyncIOMotorClient(os.environ['DB_CONNECTION_URL'])
db = db_client['myGPT']

