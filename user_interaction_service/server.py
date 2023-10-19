"""Handles User Interaction App Server"""
from sqlalchemy import inspect
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.middleware import Middleware
from starlette.middleware.cors import CORSMiddleware
from user_interaction_service.endpoints.user_interaction import UserInteractionEndpoint
from user_interaction_service.endpoints.swagger_doc import SwaggerDoc
from user_interaction_service.models import BASE, DB_ENGINE

user_interaction: UserInteractionEndpoint = UserInteractionEndpoint()
swagger_doc: SwaggerDoc = SwaggerDoc()

routes: list[Route] = [
    Route("/contents", user_interaction.fetch_like_and_read, methods=["GET"]),
    Route(
        "/content/{title}/user/{id}/like", user_interaction.add_like, methods=["POST"]
    ),
    Route(
        "/content/{title}/user/{id}/read", user_interaction.add_read, methods=["POST"]
    ),
    Route("/docs", swagger_doc.swagger_ui, methods=["GET"]),
    Route("/spec", swagger_doc.get_spec, methods=["GET"]),
]


middleware = [
    Middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    ),
]


def on_startup():
    """Check if table exist or not and create table"""
    inspector = inspect(DB_ENGINE)
    if not inspector.has_table("Interaction"):
        BASE.metadata.create_all(DB_ENGINE)


app: Starlette = Starlette(routes=routes, middleware=middleware)

app.add_event_handler("startup", on_startup)
