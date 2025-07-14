from pydantic import BaseModel, Field
from typing import Optional

class UserCreate(BaseModel):
    username: str = Field(..., example="john")
    password: str = Field(..., example="strongpassword")

class UserUpdate(BaseModel):
    password: Optional[str] = Field(None, example="newpassword123")

class UserResponse(BaseModel):
    id: int
    username: str
    role: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class ErrorResponse(BaseModel):
    detail: str
