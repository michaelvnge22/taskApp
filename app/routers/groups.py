from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models import Group, GroupMember, Invite
from app.schemas import GroupCreate, GroupResponse
from uuid import uuid4

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.post("/", response_model=GroupResponse)
def create_group(data: GroupCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = Group(name=data.name, owner_id=current_user.id)
    db.add(group)
    db.commit()
    db.refresh(group)

    # ajouter le propriétaire comme membre/admin pour qu'il voie immédiatement son groupe
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


@router.post("/{group_id}/invite")
def generate_invite(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    group = db.query(Group).get(group_id)
    if not group:
        raise HTTPException(404, "Groupe introuvable")

    if group.owner_id != current_user.id:
        raise HTTPException(403, "Seul le propriétaire peut inviter")

    token = uuid4().hex
    invite = Invite(group_id=group_id, token=token)
    db.add(invite)
    db.commit()

    return {"invite_link": f"http://127.0.0.1:8000/groups/join/{token}"}


@router.get("/join/{token}")
def join_group(token: str, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    invite = db.query(Invite).filter(Invite.token == token).first()
    if not invite:
        raise HTTPException(400, "Invitation invalide")

    membership = GroupMember(user_id=current_user.id, group_id=invite.group_id)
    db.add(membership)
    db.commit()

    return {"message": "Ajouté au groupe"}
