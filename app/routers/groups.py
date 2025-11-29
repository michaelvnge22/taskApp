# app/routers/groups.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models import Group, GroupMember, Invite, User
from app.schemas import GroupCreate, GroupResponse, GroupDetailResponse, MemberResponseSimple
from uuid import uuid4

router = APIRouter(prefix="/groups", tags=["Groups"])

@router.post("/", response_model=GroupResponse)
def create_group(data: GroupCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = Group(name=data.name, owner_id=current_user.id)
    db.add(group)
    db.commit()
    db.refresh(group)

    # add creator as admin member
    membership = GroupMember(user_id=current_user.id, group_id=group.id, role="admin")
    db.add(membership)
    db.commit()

    return group

@router.get("/", response_model=list[GroupResponse])
def list_groups(db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    groups = (
        db.query(Group)
        .join(GroupMember, GroupMember.group_id == Group.id)
        .filter(GroupMember.user_id == current_user.id)
        .all()
    )
    return groups

@router.get("/{group_id}", response_model=GroupDetailResponse)
def get_group(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(404, "Groupe introuvable")

    # load members
    members_q = (
        db.query(GroupMember, User)
        .join(User, GroupMember.user_id == User.id)
        .filter(GroupMember.group_id == group_id)
        .all()
    )

    members = []
    for gm, u in members_q:
        members.append({
            "id": gm.id,
            "user_id": u.id,
            "username": u.username,
            "email": u.email,
            "role": gm.role
        })

    return GroupDetailResponse(
        id=group.id,
        name=group.name,
        owner_id=group.owner_id,
        members=members
    )

@router.get("/{group_id}/members", response_model=list[MemberResponseSimple])
def list_group_members(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    members_q = (
        db.query(GroupMember, User)
        .join(User, GroupMember.user_id == User.id)
        .filter(GroupMember.group_id == group_id)
        .all()
    )
    members = []
    for gm, u in members_q:
        members.append({
            "id": gm.id,
            "user_id": u.id,
            "username": u.username,
            "email": u.email,
            "role": gm.role
        })
    return members

@router.delete("/{group_id}/members/{user_id}")
def remove_member(group_id: int, user_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(404, "Groupe introuvable")

    # only owner or admin can remove
    if group.owner_id != current_user.id:
        admin_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id, GroupMember.user_id == current_user.id, GroupMember.role == "admin"
        ).first()
        if not admin_membership:
            raise HTTPException(403, "Seul le propriétaire ou un admin peut retirer un membre")

    membership = db.query(GroupMember).filter(GroupMember.group_id == group_id, GroupMember.user_id == user_id).first()
    if not membership:
        raise HTTPException(404, "Membre non trouvé")

    db.delete(membership)
    db.commit()
    return {"message": "Membre retiré"}

@router.post("/{group_id}/invite")
def generate_invite(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = db.query(Group).filter(Group.id == group_id).first()
    if not group:
        raise HTTPException(404, "Groupe introuvable")

    # only owner or admin can create invite
    if group.owner_id != current_user.id:
        admin_membership = db.query(GroupMember).filter(
            GroupMember.group_id == group_id, GroupMember.user_id == current_user.id, GroupMember.role == "admin"
        ).first()
        if not admin_membership:
            raise HTTPException(403, "Seul le propriétaire ou un admin peut inviter")

    token = uuid4().hex
    invite = Invite(group_id=group_id, token=token)
    db.add(invite)
    db.commit()

    return {"invite_link": f"http://127.0.0.1:8000/groups/join/{token}", "token": token}

@router.get("/join/{token}")
def join_group(token: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    invite = db.query(Invite).filter(Invite.token == token, Invite.used == False).first()
    if not invite:
        raise HTTPException(400, "Invitation invalide ou utilisée")

    # if already member, just return
    existing = db.query(GroupMember).filter(GroupMember.group_id == invite.group_id, GroupMember.user_id == current_user.id).first()
    if existing:
        return {"message": "Déjà membre"}

    membership = GroupMember(user_id=current_user.id, group_id=invite.group_id, role="member")
    db.add(membership)
    # mark invite used
    invite.used = True
    db.commit()

    return {"message": "Ajouté au groupe"}
