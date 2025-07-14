from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from app.schemas import UserCreate, UserResponse, UserUpdate, Token, ErrorResponse
from app.db import get_async_session, get_user_repository
from app.auth import get_current_user, create_access_token, verify_password, hash_password
from sqlalchemy.ext.asyncio import AsyncSession
from app.models import User

router = APIRouter()

@router.post("/register", response_model=UserResponse, status_code=status.HTTP_201_CREATED,
    responses={400: {"model": ErrorResponse, "description": "Username taken", "content": {"application/json": {"example": {"detail": "Username already exists"}}}}},
    summary="Register a new user")
async def register(user: UserCreate, session: AsyncSession = Depends(get_async_session)):
    repo = get_user_repository(session)
    existing = await repo.get_by_username(user.username)
    if existing:
        return JSONResponse(status_code=400, content={"detail": "Username already exists"})
    hashed_pw = hash_password(user.password)
    db_user = await repo.create_user(username=user.username, password=hashed_pw, role="user")
    return UserResponse.from_orm(db_user)

@router.post("/login", response_model=Token, responses={
    401: {"model": ErrorResponse, "description": "Invalid credentials", "content": {"application/json": {"example": {"detail": "Incorrect username or password"}}}}
    }, summary="Authenticate and get JWT access token")
async def login(data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    repo = get_user_repository(session)
    user: User = await repo.get_by_username(data.username)
    if not user or not verify_password(data.password, user.password):
        return JSONResponse(status_code=401, content={"detail": "Incorrect username or password"})
    access_token = create_access_token({"sub": user.username, "role": user.role})
    return Token(access_token=access_token, token_type="bearer")

@router.get("/me", response_model=UserResponse, summary="Get current user profile")
async def get_profile(current_user: User = Depends(get_current_user)):
    return UserResponse.from_orm(current_user)

@router.put("/me", response_model=UserResponse, summary="Update current user profile")
async def update_profile(update: UserUpdate, session: AsyncSession = Depends(get_async_session), current_user: User = Depends(get_current_user)):
    repo = get_user_repository(session)
    # Only allow updating password
    hashed_pw = hash_password(update.password) if update.password else None
    user = await repo.update_user(current_user.id, hashed_pw)
    return UserResponse.from_orm(user)
