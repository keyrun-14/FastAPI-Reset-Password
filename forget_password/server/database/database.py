# Motor, an asynchronous MongoDB driver, to interact with the database.
import motor.motor_asyncio

from server.utilities import settings

MONGO_DETAILS = settings.mongodb_uri

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS) # connecting mongodb cluster.

database = client.users # creating database as users

user_collection = database.get_collection("user_details") # creating collection as user_collection

# When the first I/O operation is made, 
# both the database and collection will be created if they don't already exist.