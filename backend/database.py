from model import Rental

# MongoDB driver
import motor.motor_asyncio

client = motor.motor_asyncio.AsyncIOMotorClient(
    'mongodb://localhost:27017')

database = client.Rent4Hire
collection = database.rental

async def fetch_one_rental(name):
    document = await collection.find_one({"name":name})
    return document