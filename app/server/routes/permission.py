from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database.permission import (
    add_permission,
    delete_permission,
    retrieve_permission,
    retrieve_permissions,
    update_permission,
)
from server.models.permission import (
    ErrorResponseModel,
    ResponseModel,
    PermissionSchema,
    UpdatePermissionModel,
)

router = APIRouter()

@router.post("/", response_description="permission data added into the database")
async def add_permission_data(permission: PermissionSchema = Body(...)):
    permission = jsonable_encoder(permission)
    print("Permission before encoding", permission)
    new_permission = await add_permission(permission)
    if new_permission:
        return ResponseModel(new_permission, "permission added successfully.")
    return ResponseModel(new_permission, "Invalid Parameters")

@router.get("/", response_description="permissions retrieved")
async def get_permissions():
    permissions = await retrieve_permissions()
    if permissions:
        return ResponseModel(permissions, "permissions data retrieved successfully")
    return ResponseModel(permissions, "Empty list returned")


@router.get("/{id}", response_description="permission data retrieved")
async def get_permission_data(id):
    permission = await retrieve_permission(id)
    if permission:
        return ResponseModel(permission, "permission data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "permission doesn't exist.")


@router.put("/{id}")
async def update_permission_data(id: str, req: UpdatePermissionModel = Body(...)):
    req = {k: v for k, v in req.dict().items() if v is not None}
    updated_permission = await update_permission(id, req)
    if updated_permission:
        return ResponseModel(
            "permission with ID: {} name update is successful".format(id),
            "permission name updated successfully",
        )
    return ErrorResponseModel(
        "An error occurred",
        404,
        "There was an error updating the permission data.",
    )


@router.delete("/{id}", response_description="permission data deleted from the database")
async def delete_permission_data(id: str):
    deleted_permission = await delete_permission(id)
    if deleted_permission:
        return ResponseModel(
            "permission with ID: {} removed".format(id), "permission deleted successfully"
        )
    return ErrorResponseModel(
        "An error occurred", 404, "permission with id {0} doesn't exist".format(id)
    )