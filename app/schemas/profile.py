from pydantic import BaseModel
from typing import Optional

class ProfileResponse(BaseModel):
    id: str
    email: str
    name: Optional[str]
    bio: Optional[str]

    class Config:
        from_attributes = True

class ProfileUpdateRequest(BaseModel):
    name: Optional[str] = None
    bio: Optional[str] = None

class ProfileDeleteRequest(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None