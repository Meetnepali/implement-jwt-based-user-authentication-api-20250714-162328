from fastapi import FastAPI
from app.routers import users, admin
from app.errors import add_custom_error_handlers

app = FastAPI(title="SaaS User Management API", description="User management with JWT auth and role-based admin features.", version="1.0.0")

# Register routers
def register_routers(app):
    app.include_router(users.router, prefix="/users", tags=["Users"])
    app.include_router(admin.router, prefix="/admin", tags=["Admin"])

register_routers(app)
add_custom_error_handlers(app)
