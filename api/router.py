from fastapi import APIRouter

api = APIRouter(prefix="/api")

root = APIRouter(generate_unique_id_function=lambda route: f"{route.name}")
root.include_router(api)
