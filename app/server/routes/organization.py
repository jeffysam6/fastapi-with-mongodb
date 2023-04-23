from fastapi import APIRouter, Body
from fastapi.encoders import jsonable_encoder

from server.database.organization import (
    add_organization,
    retrieve_organization,
    retrieve_organizations,
)
from server.models.organization import (
    ErrorResponseModel,
    ResponseModel,
    OrganizationSchema,
)

router = APIRouter()

@router.post("/", response_description="organization data added into the database")
async def add_organization_data(organization: OrganizationSchema = Body(...)):
    print("Adding organization data", organization)
    organization = jsonable_encoder(organization)
    print("After encoding data", organization)
    new_organization = await add_organization(organization)
    print("Response After encoding data", new_organization)
    return ResponseModel(new_organization, "organization added successfully.")


@router.get("/", response_description="organizations retrieved")
async def get_organizations(name: str = None, limit: int = 5, offset: int = 0):
    organizations = await retrieve_organizations(name, limit, offset)
    print("Get organizations", organizations)
    if organizations:
        return ResponseModel(organizations, "organizations data retrieved successfully")
    return ResponseModel(organizations, "Empty list returned")


@router.get("/{id}", response_description="organization data retrieved")
async def get_organization_data(id):
    organization = await retrieve_organization(id)
    if organization:
        return ResponseModel(organization, "organization data retrieved successfully")
    return ErrorResponseModel("An error occurred.", 404, "organization doesn't exist.")

