from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder
from bson import ObjectId

from server.database.user import (
    add_user,
    retrieve_user,
    retrieve_users,
)
from server.models.user import (
    ErrorResponseModel,
    ResponseModel,
    UserSchema,
)

router = APIRouter()

@router.post("/", response_description="user data added into the database")
async def add_user_data(user: UserSchema = Body(...)):
    print("Adding user data", user)
    user = jsonable_encoder(user)
    print("After encoding data", user)
    user['_id'] = ObjectId(user['_id'])
    new_user = await add_user(user)
    print("Response After encoding data", new_user)
    return ResponseModel(new_user, "Student added successfully.")


@router.get("/", response_description="users retrieved")
async def get_users(limit: int = 5, offset: int = 0):
    users = await retrieve_users(limit, offset)
    print("Get users", users)
    if users:
        return ResponseModel(users, "users data retrieved successfully")
    return ResponseModel(users, "Empty list returned")


@router.get("/{id}", response_description="user data retrieved")
async def get_user_data(id):
    user = await retrieve_user(id)
    if user:
        return ResponseModel(user, "user data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "user doesn't exist.")

