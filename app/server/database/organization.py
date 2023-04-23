import motor.motor_asyncio
from bson.objectid import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.cosmo_admin

organization_collection = database.get_collection("organizations")


organization_collection.create_index("name", unique=True)


def organization_helper(organization) -> dict:
    return {
        "id": str(organization["_id"]),
        "name": organization["name"],
    }

async def retrieve_organizations(name, limit, offset):
    organizations = []
    filter = {}

    if name:
        filter['name'] = {'$regex': f'^{name}', '$options': 'i'} 

    async for organization in organization_collection.find(filter).skip(offset).limit(limit):
        organizations.append(organization_helper(organization))
    return organizations


async def add_organization(organization_data: dict) -> dict:
    organization = await organization_collection.insert_one(organization_data)
    new_organization = await organization_collection.find_one({"_id": organization.inserted_id})
    return organization_helper(new_organization)


async def retrieve_organization(name: str) -> dict:
    search_term = f"^{name}"
    organization = await organization_collection.find_one({"name": name}) 
    if organization:
        return organization_helper(organization)

