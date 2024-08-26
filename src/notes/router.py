from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.exc import NoResultFound

from ..database import get_async_session
from .models import Note
from .schemas import NoteCreate, NoteRead, NoteUpdate
from .validators import check_spelling
from ..auth.models import User
from ..base import current_user

router = APIRouter()

@router.get("/notes/", response_model=List[NoteRead])
async def get_user_notes(
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(select(Note).where(Note.creator_id == user.id))
    notes = result.scalars().all()
    return notes

@router.post("/notes/", response_model=NoteRead, status_code=status.HTTP_201_CREATED)
async def create_note(
    note_data: NoteCreate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    spelling_errors = await check_spelling(note_data.content)
    
    if spelling_errors:
        error_messages = [
            f"Ошибка в слове '{error['word']}'. Возможно, имелось в виду: {', '.join(error['s'])}"
            for error in spelling_errors
        ]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Обнаружены орфографические ошибки.", "errors": error_messages}
        )

    new_note = Note(
        content=note_data.content,
        creator_id=user.id,
    )
    session.add(new_note)
    await session.commit()
    await session.refresh(new_note)
    return new_note

@router.get("/notes/{note_id}", response_model=NoteRead)
async def get_note_by_id(
    note_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(Note).where(Note.id == note_id, Note.creator_id == user.id)
        )
        note = result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")
    return note

@router.put("/notes/{note_id}", response_model=NoteRead)
async def update_note(
    note_id: int,
    note_data: NoteUpdate,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(Note).where(Note.id == note_id, Note.creator_id == user.id)
        )
        note = result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    spelling_errors = await check_spelling(note_data.content)
    
    if spelling_errors:
        error_messages = [
            f"Ошибка в слове '{error['word']}'. Возможно, имелось в виду: {', '.join(error['s'])}"
            for error in spelling_errors
        ]
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"message": "Обнаружены орфографические ошибки.", "errors": error_messages}
        )

    note.content = note_data.content
    await session.commit()
    await session.refresh(note)
    return note

@router.delete("/notes/{note_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_note(
    note_id: int,
    user: User = Depends(current_user),
    session: AsyncSession = Depends(get_async_session)
):
    try:
        result = await session.execute(
            select(Note).where(Note.id == note_id, Note.creator_id == user.id)
        )
        note = result.scalar_one()
    except NoResultFound:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Note not found")

    await session.delete(note)
    await session.commit()
    return None