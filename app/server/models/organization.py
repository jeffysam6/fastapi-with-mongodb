from typing import Optional, List
from pydantic import BaseModel, Field
from enum import Enum

class AccessLevel(str, Enum):
    READ = "READ"
    WRITE = "WRITE"
    ADMIN = "ADMIN"

### This is another way of rewriting the schema ###
# class OrganizationPermissionSchema(BaseModel):
#     user_id: str
#     access_level: AccessLevel


class OrganizationSchema(BaseModel):
    name: str = Field(..., unique=True)
    # users: Optional[List[OrganizationPermissionSchema]] # A List of Users 
       
    class Config:
        collection = "organizations"
        indexes = [{'fields': ['name'], 'unique': True}]
        schema_extra = {
            "example": {
                "name": "Google",
            }
        }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
        "total_count": len(data) if isinstance(data, list) else 1
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}