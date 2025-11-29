# app/routers/tasks.py
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.core.security import get_current_user
from app.models import Task, Group
from app.schemas import TaskCreate, TaskUpdate, TaskResponse

router = APIRouter(prefix="/tasks", tags=["Tasks"])

@router.post("/", response_model=TaskResponse)
def create_task(data: TaskCreate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    if data.group_id is not None:
        group = db.query(Group).filter(Group.id == data.group_id).first()
        if not group:
            raise HTTPException(404, "Groupe introuvable")

    task = Task(
        title=data.title,
        description=data.description or "",
        status=data.status or "todo",
        deadline=data.deadline,
        group_id=data.group_id,
        creator_id=current_user.id
    )
    db.add(task)
    db.commit()
    db.refresh(task)
    return task

@router.get("/group/{group_id}", response_model=list[TaskResponse])
def list_group_tasks(group_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    tasks = db.query(Task).filter(Task.group_id == group_id).all()
    return tasks

@router.put("/{task_id}", response_model=TaskResponse)
def update_task(task_id: int, data: TaskUpdate, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(404, "Tâche introuvable")

    # only creator or group admin/owner could update in production; here we allow creator
    if task.creator_id != current_user.id:
        # optional: allow group owner/admin (not implemented fully)
        pass

    for key, value in data.dict(exclude_unset=True).items():
        setattr(task, key, value)

    db.commit()
    db.refresh(task)
    return task

@router.delete("/{task_id}")
def delete_task(task_id: int, db: Session = Depends(get_db), current_user=Depends(get_current_user)):
    task = db.query(Task).get(task_id)
    if not task:
        raise HTTPException(404, "Tâche introuvable")

    db.delete(task)
    db.commit()
    return {"message": "Tâche supprimée"}
