from pydantic import BaseModel

# Create User Schema (Pydantic Model)
class UserCreate(BaseModel):
    name: str
    age: int
    gender: str
    address: str

# Complete User Schema (Pydantic Model)
class User(BaseModel):
    id: int
    name: str
    age: int
    gender: str
    address: str

    class Config:
        orm_mode = True