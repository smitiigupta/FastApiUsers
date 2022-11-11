from pydantic import BaseModel

# Create User Schema (Pydantic Model)
class UserCreate(BaseModel):
    name: str

# Complete User Schema (Pydantic Model)
class User(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True