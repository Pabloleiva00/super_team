from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models.videoCall import VideoCall
from database import get_db
from pydantic import BaseModel
from datetime import datetime
from schemas.videoCall import VideoCallCreate, VideoCallUpdate

router = APIRouter()

# crear llamadas
@router.post("/")
async def create_video_call(video_call: VideoCallCreate, db: Session = Depends(get_db)):
    new_call = VideoCall(
        caller_id=video_call.caller_id,
        receiver_id=video_call.receiver_id,
        started_at=video_call.started_at,
        ended_at=video_call.ended_at,
        duration=video_call.duration,
        status=video_call.status
    )
    db.add(new_call)
    db.commit()
    db.refresh(new_call)
    return new_call

# info de todas las videollamadas
@router.get("/")
async def get_all_video_calls(db: Session = Depends(get_db)):
    calls = db.query(VideoCall).all()
    if not calls:
        raise HTTPException(status_code=404, detail="No video calls found")
    return calls

# info de una llamada con id especifico
@router.get("/{call_id}")
async def get_video_call(call_id: int, db: Session = Depends(get_db)):
    call = db.query(VideoCall).filter(VideoCall.id == call_id).first()    
    if not call:
        raise HTTPException(status_code=404, detail="Video call not found")    
    return call


# encontrar llamadas pertenecientes a un usuario (remitente o receptor)
# @router.get("/users/{user_id}")
# async def get_video_calls(user_id: int, db: Session = Depends(get_db)):
#     calls = db.query(VideoCall).filter(
#         (VideoCall.caller_id == user_id) | (VideoCall.receiver_id == user_id)
#     ).all()
#     if not calls:
#         raise HTTPException(status_code=404, detail="No calls found")
#     return calls

from sqlalchemy import desc, or_
from datetime import timedelta

@router.get("/users/{user_id}")
async def get_video_calls(user_id: int, db: Session = Depends(get_db)):
    all_calls = db.query(VideoCall).filter(
        or_(
            VideoCall.caller_id == user_id,
            VideoCall.receiver_id == user_id
        )
    ).order_by(desc(VideoCall.started_at)).all()

    unique_calls = []

    for call in all_calls:
        is_duplicate = False
        for saved_call in unique_calls:
            time_diff = abs((call.started_at - saved_call.started_at).total_seconds())
            same_pair = (
                {call.caller_id, call.receiver_id} == {saved_call.caller_id, saved_call.receiver_id}
            )
            if same_pair and time_diff < 60:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_calls.append(call)
    return [to_dict(call) for call in unique_calls]

from datetime import timezone, timedelta
def to_dict(call):
    utc_minus_4 = timezone(timedelta(hours=-4))
    return {
        "id": call.id,
        "caller_id": call.caller_id,
        "receiver_id": call.receiver_id,
        "created_at": call.created_at.astimezone(utc_minus_4) if call.created_at else None,
        "started_at": call.started_at.astimezone(utc_minus_4) if call.started_at else None,
        "ended_at": call.ended_at.astimezone(utc_minus_4) if call.ended_at else None,
        "updated_at": call.updated_at.astimezone(utc_minus_4) if call.updated_at else None,
        "duration": call.duration,
        "status": call.status,
    }

# modificar llamadas
@router.put("/{call_id}")
async def update_video_call(call_id: int, video_call_update: VideoCallUpdate, db: Session = Depends(get_db)):
    db_call = db.query(VideoCall).filter(VideoCall.id == call_id).first()
    if not db_call:
        raise HTTPException(status_code=404, detail="Video call not found")
    if video_call_update.started_at:
        db_call.started_at = video_call_update.started_at
    if video_call_update.ended_at:
        db_call.ended_at = video_call_update.ended_at
        video_call_update.status = "finished"
    if video_call_update.duration is not None:
        db_call.duration = video_call_update.duration
    if video_call_update.status:
        db_call.status = video_call_update.status

    db.commit()
    db.refresh(db_call)
    return db_call

# modificar llamadas parcialmente
@router.patch("/{call_id}")
async def update_video_call(call_id: int, video_call_update: VideoCallUpdate, db: Session = Depends(get_db)):
    db_call = db.query(VideoCall).filter(VideoCall.id == call_id).first()
    if not db_call:
        raise HTTPException(status_code=404, detail="Video call not found")
    if video_call_update.started_at not in [None, ""]:
        db_call.started_at = video_call_update.started_at
    if video_call_update.ended_at not in [None, ""]:
        db_call.ended_at = video_call_update.ended_at
    if video_call_update.duration not in [None, ""]:
        db_call.duration = video_call_update.duration
    if video_call_update.status not in [None, ""]:
        db_call.status = video_call_update.status
    db.commit()
    db.refresh(db_call)
    return db_call

# eliminar una llamada
@router.delete("/{call_id}")
async def delete_video_call(call_id: int, db: Session = Depends(get_db)):
    db_call = db.query(VideoCall).filter(VideoCall.id == call_id).first()
    if not db_call:
        raise HTTPException(status_code=404, detail="Video call not found")

    db.delete(db_call)
    db.commit()
    return {"detail": "Video call deleted successfully"}