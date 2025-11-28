from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Boolean, Text
from sqlalchemy.orm import relationship
from datetime import datetime
from app.database import Base

###############################################################################
# USER
###############################################################################

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    groups = relationship("Group", back_populates="owner")
    memberships = relationship("GroupMember", back_populates="user")
    tasks = relationship("Task", back_populates="creator")


###############################################################################
# GROUP
###############################################################################

class Group(Base):
    __tablename__ = "groups"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id"))
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relations
    owner = relationship("User", back_populates="groups")
    members = relationship("GroupMember", back_populates="group")
    tasks = relationship("Task", back_populates="group")


###############################################################################
# GROUP MEMBERSHIP
###############################################################################

class GroupMember(Base):
    __tablename__ = "group_members"

    id = Column(Integer, primary_key=True, index=True)
    group_id = Column(Integer, ForeignKey("groups.id"))
    user_id = Column(Integer, ForeignKey("users.id"))
    role = Column(String, default="member")  # member/admin

    # Relations
    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="memberships")


###############################################################################
# INVITATION TOKENS
###############################################################################

class Invite(Base):
    __tablename__ = "invites"

    id = Column(Integer, primary_key=True, index=True)
    token = Column(String, unique=True, index=True, nullable=False)
    group_id = Column(Integer, ForeignKey("groups.id"))
    invited_email = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    used = Column(Boolean, default=False)


###############################################################################
# TASK
###############################################################################

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, default="")
    status = Column(String, default="todo")  # todo / inprogress / done
    deadline = Column(DateTime, nullable=True)
    creator_id = Column(Integer, ForeignKey("users.id"))
    group_id = Column(Integer, ForeignKey("groups.id"), nullable=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relations
    creator = relationship("User", back_populates="tasks")
    group = relationship("Group", back_populates="tasks", lazy="joined")