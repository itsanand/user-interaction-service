"""Handles User Interaction App Server"""
from starlette.applications import Starlette
from starlette.routing import Route
from user_interaction_service.endpoints.user_interaction import UserInteractionEndpoint

user_interaction: UserInteractionEndpoint = UserInteractionEndpoint()

routes: list[Route] = [
    Route(
        "/content/{title}/user/{id}/like", user_interaction.add_like, methods=["POST"]
    ),
    Route(
        "/content/{title}/user/{id}/read", user_interaction.add_read, methods=["POST"]
    ),
    Route("/content/{title}", user_interaction.fetch_like_and_read, methods=["GET"]),
]

app: Starlette = Starlette(routes=routes)
