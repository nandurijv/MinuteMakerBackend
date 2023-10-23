import uuid
from pydantic import BaseModel, Field

class User(BaseModel):
    id: str = Field(default_factory=uuid.uuid4, alias="_id")
    name: str
    email: str
    password: str
    phone: int
    country_code: int = "91"
    verified: int = "0"

    class Config:
        populate_by_name = True
        json_schema_extra = {
            "example": {
                "name":"Nanduri Jayant Vishnu",
                "email":"vishnunanduri8@gmail.com",
                "verified":"0",
                "phone":"8219672467",
                "country_code":"91"
            }
        }