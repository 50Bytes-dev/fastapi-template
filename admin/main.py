from sqladmin import Admin

from admin.auth import AdminAuth
from config import get_settings
from core.db import async_engine

settings = get_settings()


def create_admin_panel(app):
    admin = Admin(
        app=app,
        authentication_backend=AdminAuth(secret_key=settings.APP_SECRET_KEY),
        engine=async_engine,
    )

    # Example of adding a model to the admin panel
    # admin.add_view(UserAdmin)

    return admin
