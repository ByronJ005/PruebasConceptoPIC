import re
from uuid import UUID
from pydantic import BaseModel, EmailStr, field_validator, Field

# Regular expression for password complexity: at least 1 number and 1 special character
PASSWORD_REGEX = re.compile(r"^(?=.*[0-9])(?=.*[!@#$%^&*(),.?\":{}|<>]).*$")

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters long")

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        if not PASSWORD_REGEX.match(v):
            raise ValueError("Password must contain at least one number and one special character")
        return v

class UserLogin(UserBase):
    password: str

class UserResponse(UserBase):
    id: UUID
    is_active: bool

    class Config:
        from_attributes = True

class Token(BaseModel):
    access_token: str
    token_type: str

class PasswordRecoveryRequest(UserBase):
    pass

class PasswordReset(BaseModel):
    token: str
    new_password: str = Field(..., min_length=8)

    @field_validator("new_password")
    @classmethod
    def validate_new_password_complexity(cls, v: str) -> str:
        if not PASSWORD_REGEX.match(v):
            raise ValueError("Password must contain at least one number and one special character")
        return v
