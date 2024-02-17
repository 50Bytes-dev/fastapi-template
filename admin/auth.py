from sqladmin.authentication import AuthenticationBackend

from fastapi import Request


class AdminAuth(AuthenticationBackend):

    async def login(
        self,
        request: Request,
    ) -> bool:
        form = await request.form()
        username, password = form["username"], form["password"]
        if username != "admin" or password != "abrakadabra":
            return False

        request.session.update({"is_authenticated": "true"})

        return True

    async def logout(
        self,
        request: Request,
    ) -> bool:
        request.session.clear()
        return True

    async def authenticate(
        self,
        request: Request,
    ):
        is_authenticated = request.session.get("is_authenticated")

        if not is_authenticated:
            return False

        return True
