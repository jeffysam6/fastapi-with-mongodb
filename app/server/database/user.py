import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cosmo_admin

user_collection = database.get_collection("users")

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "email": user["email"],
    }

# Retrieve all users present in the database
async def retrieve_users(limit, offset):
    users = []
    async for user in user_collection.find().skip(offset).limit(limit):
        users.append(user_helper(user))
    return users


# Add a new user into to the database
async def add_user(user_data: dict) -> dict:
    print("user data", user_data)
    user = await user_collection.insert_one(user_data)
    print("inserted user", user)
    new_user = await user_collection.find_one({"_id": user.inserted_id})
    print("new user", new_user)
    return user_helper(new_user)


# Retrieve a user with a matching ID
async def retrieve_user(id: str) -> dict:
    user = await user_collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)

