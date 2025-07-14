import pytest
from httpx import AsyncClient
from app.main import app
import asyncio
import os
import pytest

@pytest.mark.asyncio
async def test_user_workflow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register as a normal user
        res = await ac.post("/users/register", json={"username": "alice", "password": "alicepass"})
        assert res.status_code == 201
        user_id = res.json()["id"]
        # Login as user
        res = await ac.post("/users/login", json={"username": "alice", "password": "alicepass"})
        assert res.status_code == 200
        token = res.json()["access_token"]
        # Get profile
        res = await ac.get("/users/me", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert res.json()["username"] == "alice"
        # Update password
        res = await ac.put("/users/me", json={"password": "newalicepass"}, headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        # List users (should fail)
        res = await ac.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 403 or res.status_code == 401

@pytest.mark.asyncio
async def test_admin_workflow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        # Register admin user
        res = await ac.post("/users/register", json={"username": "admin", "password": "adminpass"})
        assert res.status_code == 201
        # Manually promote to admin for test
        from app.db import async_session, UserRepository
        async with async_session() as session:
            repo = UserRepository(session)
            user = await repo.get_by_username("admin")
            await session.execute(
                user.__table__.update().where(user.__table__.c.id == user.id).values(role="admin")
            )
            await session.commit()
        # Login as admin
        res = await ac.post("/users/login", json={"username": "admin", "password": "adminpass"})
        assert res.status_code == 200
        token = res.json()["access_token"]
        # List users
        res = await ac.get("/admin/users", headers={"Authorization": f"Bearer {token}"})
        assert res.status_code == 200
        assert isinstance(res.json(), list)
        # Delete user
        users = res.json()
        user_to_delete = [u for u in users if u["username"] != "admin"]
        if user_to_delete:
            uid = user_to_delete[0]["id"]
            res = await ac.delete(f"/admin/users/{uid}", headers={"Authorization": f"Bearer {token}"})
            assert res.status_code == 204
