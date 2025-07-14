from fastapi import APIRouter, Depends, status
from app.db import get_async_session, get_user_repository
from app.auth import get_current_active_admin
from app.schemas import UserResponse, ErrorResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter()

@router.get("/users", response_model=list[UserResponse], summary="List all users (admin only)",
    responses={403: {"model": ErrorResponse, "description": "Forbidden: Admin only", "content": {"application/json": {"example": {"detail": "Not enough permissions"}}}}})
async def list_users(session: AsyncSession = Depends(get_async_session), current_admin=Depends(get_current_active_admin)):
    repo = get_user_repository(session)
    users = await repo.list_users()
    return [UserResponse.from_orm(u) for u in users]

@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a user (admin only)",
    responses={403: {"model": ErrorResponse, "description": "Forbidden: Admin only", "content": {"application/json": {"example": {"detail": "Not enough permissions"}}}}, 404: {"model": ErrorResponse, "description": "Not found", "content": {"application/json": {"example": {"detail": "User not found"}}}}})
async def delete_user(user_id: int, session: AsyncSession = Depends(get_async_session), current_admin=Depends(get_current_active_admin)):
    repo = get_user_repository(session)
    deleted = await repo.delete_user(user_id)
    if not deleted:
        return ErrorResponse(detail="User not found")
    return
