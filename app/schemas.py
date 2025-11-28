from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, EmailStr

# -----------------------------
# USER SCHEMAS
# -----------------------------
class UserBase(BaseModel):
    email: EmailStr

class UserCreate(BaseModel):
    email: str
    username: str
    password: str

class UserResponse(UserBase):
    id: int

    class Config:
        orm_mode = True

# -----------------------------
# AUTH SCHEMAS
# -----------------------------
class LoginSchema(BaseModel):
    email: str
    password: str

class RegisterSchema(BaseModel):
    email: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    user_id: Optional[int] = None

# -----------------------------
# GROUP SCHEMAS
# -----------------------------
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int

    class Config:
        orm_mode = True

# -----------------------------
# MEMBERSHIP
# -----------------------------
class MemberResponse(BaseModel):
    id: int
    user_id: int
    group_id: int

    class Config:
        orm_mode = True

# -----------------------------
# INVITE SCHEMAS
# -----------------------------
class InviteCreate(BaseModel):
    group_id: int

class InviteResponse(BaseModel):
    id: int
    token: str
    group_id: int

    class Config:
        orm_mode = True

# -----------------------------
# TASK SCHEMAS
# -----------------------------
class TaskBase(BaseModel):
    title: str
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[str] = "pending"

class TaskCreate(TaskBase):
    group_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[str] = None

class TaskResponse(TaskBase):
    id: int
    group_id: Optional[int] = None
    group: Optional[GroupResponse] = None
    created_at: datetime

    class Config:
        orm_mode = True
