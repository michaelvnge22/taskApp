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
    username: str
    
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
# MEMBERSHIP
# -----------------------------
class MemberResponseSimple(BaseModel):
    id: int
    user_id: int
    username: str
    email: str
    role: str
    #group_id: int

    class Config:
        orm_mode = True


# -----------------------------
# GROUP SCHEMAS
# -----------------------------
class GroupBase(BaseModel):
    name: str

class GroupCreate(GroupBase):
    pass

class GroupResponse(GroupBase):
    id: int
    owner_id: Optional[int] = None

    class Config:
        orm_mode = True

class GroupDetailResponse(GroupResponse):
    members: List[MemberResponseSimple] = []


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
    status: Optional[str] = "todo"

class TaskCreate(TaskBase):
    group_id: Optional[int] = None

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    deadline: Optional[date] = None
    status: Optional[str] = None
    group_id: Optional[int] = None

class TaskResponse(TaskBase):
    id: int
    group_id: Optional[int] = None
    group: Optional[GroupResponse] = None
    created_at: datetime

    class Config:
        from_attributes = True
