from typing import Optional

from pydantic import BaseModel, EmailStr, Field
from bson import ObjectId
from bson.json_util import loads, dumps

# class PyObjectId(ObjectId):
#     @classmethod
#     def __get_validators__(cls):
#         yield cls.validate
#     @classmethod
#     def validate(cls, v):
#         if not ObjectId.is_valid(v):
#             raise ValueError("Invalid objectid")
#         return ObjectId(v)
#     @classmethod
#     def __modify_schema__(cls, field_schema):
#         field_schema.update(type="string")


class UserSchema(BaseModel):
    id: str = Field(default_factory=lambda: str(ObjectId()), alias="_id")
    fullname: str = Field(...)
    email: EmailStr = Field(...)
    
    __collection__ = "users"
   
    class Config:
        json_loads = loads  # Use bson.json_util.loads for deserialization
        json_dumps = dumps  # Use bson.json_util.dumps for serialization
        allow_population_by_field_name = True  # Enable population by field name
        use_enum_values = True  # Use enum values instead of names
        arbitrary_types_allowed = True  # Allow arbitrary types
        schema_extra = {
            "example": {
                "fullname": "John Doe",
                "email": "jdoe@x.edu.ng",
            }
        }


# class UpdateStudentModel(BaseModel):
#     fullname: Optional[str]
#     email: Optional[EmailStr]

#     class Config:
#         schema_extra = {
#             "example": {
#                 "fullname": "John Doe",
#                 "email": "jdoe@x.edu.ng",
#             }
#         }


def ResponseModel(data, message):
    return {
        "data": [data],
        "code": 200,
        "message": message,
        "total_count": len(data) if isinstance(data, list) else 1
    }


def ErrorResponseModel(error, code, message):
    return {"error": error, "code": code, "message": message}