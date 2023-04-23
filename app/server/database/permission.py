import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cosmo_admin

permission_collection = database.get_collection("permissions")
user_collection = database.get_collection("users")
organization_collection = database.get_collection("organizations")

permission_collection.create_index(
    [("user_id", 1), ("org_name", 1), ("access_level", 1)],
    unique=True
)

def permission_helper(permission) -> dict:
    return {
        "id": str(permission["_id"]),
        "user_id": permission["user_id"],
        "org_name": permission["org_name"],
        "access_level": permission["access_level"],
    }

# Retrieve all permissions present in the database
async def retrieve_permissions():
    permissions = []
    async for permission in permission_collection.find():
        permissions.append(permission_helper(permission))
    return permissions


# Add a new permission into to the database
async def add_permission(permission_data: dict) -> dict:
    filter = {}
    user_id = permission_data['user_id']
    org_name = permission_data['org_name']
    if permission_data['org_name']:
        filter['name'] = {'$regex': f'^{org_name}', '$options': 'i'}
    user = await user_collection.find_one({"_id": ObjectId(user_id)})
    org = await organization_collection.find_one(filter)
    print("Searched user and org", user, org)
    if user and org:
        permission = await permission_collection.insert_one(permission_data)
        update_data = {
        'users': {
            'user_id': user_id,
            'access_level': permission_data['access_level']
            }
        }
    # We can push it to the Organization Users list for the optimized solution
    #     await organization_collection.update_one(
    #     {'id': org['_id']},
    #     {'$push': update_data}
    # )

        new_permission = await permission_collection.find_one({"_id": permission.inserted_id})
        return permission_helper(new_permission)


# Retrieve a permission with a matching ID
async def retrieve_permission(id: str) -> dict:
    permission = await permission_collection.find_one({"_id": ObjectId(id)})
    if permission:
        return permission_helper(permission)


# Update a permission with a matching ID
async def update_permission(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    permission = await permission_collection.find_one({"_id": ObjectId(id)})
    if permission:
        updated_permission = await permission_collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_permission:
            return True
        return False


# Delete a permission from the database
async def delete_permission(id: str):
    permission = await permission_collection.find_one({"_id": ObjectId(id)})
    if permission:
        await permission_collection.delete_one({"_id": ObjectId(id)})
        return True