from typing import Optional
from enum import Enum

from pydantic import BaseModel, EmailStr, Field, validator

class AccessLevel(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"

class PermissionSchema(BaseModel):
    user_id: str
    org_name: str
    access_level: AccessLevel


    __collection__ = "permissions"
    
    @validator('access_level')
    def validate_access_level(cls, value):
        if value not in AccessLevel:
            raise ValueError("Invalid access level.")
        return value
    
    class Config:
        schema_extra = {
            "example": {
                "user_id": "",
                "org_name": "",
                "access_level": "READ",
            }
        }


class UpdatePermissionModel(BaseModel):
    user_id: Optional[str]
    org_name: Optional[str]
    access_level: Optional[str]

    class Config:
        schema_extra = {
            "example": {
                "user_id": "",
                "org_name": "",
                "access_level": "READ",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}