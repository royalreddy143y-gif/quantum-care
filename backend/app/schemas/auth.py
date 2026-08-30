from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


class UserBase(BaseModel):
    email: EmailStr
    full_name: str
    institution: Optional[str] = "QuantumCare Medical Institute"
    role: Optional[str] = "researcher"


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str
    password: str = Field(..., min_length=6)
    institution: Optional[str] = "QuantumCare Medical Institute"
    role: Optional[str] = "researcher"


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserOut(UserBase):
    id: int
    is_active: bool
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class TokenData(BaseModel):
    user_id: Optional[int] = None


class ForgotPasswordRequest(BaseModel):
    email: EmailStr


class ResetPasswordRequest(BaseModel):
    email: EmailStr
    reset_code: str = Field(..., min_length=4)
    new_password: str = Field(..., min_length=6)


class ProfileUpdateRequest(BaseModel):
    full_name: Optional[str] = Field(None, min_length=2)
    email: Optional[EmailStr] = None
    institution: Optional[str] = None


class ChangePasswordRequest(BaseModel):
    current_password: str
    new_password: str = Field(..., min_length=6)
