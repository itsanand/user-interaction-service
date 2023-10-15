"""Handles User Interaction App Server"""
from starlette.applications import Starlette
from starlette.routing import Route
from user_interaction_service.endpoints.user_interaction import UserInteractionEndpoint

user_interaction: UserInteractionEndpoint = UserInteractionEndpoint()

routes: list[Route] = [
    Route("/contents", user_interaction.fetch_like_and_read, methods=["GET"]),
    Route(
        "/content/{title}/user/{id}/like", user_interaction.add_like, methods=["POST"]
    ),
    Route(
        "/content/{title}/user/{id}/read", user_interaction.add_read, methods=["POST"]
    ),
]

app: Starlette = Starlette(routes=routes)
