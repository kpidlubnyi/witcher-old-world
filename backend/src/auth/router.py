from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

import src.auth.services.oauth.google as google_auth 
import src.auth.services.oauth.github as github_auth

from ..database import get_db
from ..lobbies.router import CurrentUserDependency
from .schemas import UserPublic


auth_router = APIRouter(prefix='/auth')


@auth_router.get("/google/url")
def get_google_auth_url():
    uri = google_auth.generate_oauth_redirect_uri()
    return RedirectResponse(url=uri)


@auth_router.get("/github/url")
def github_auth_url():
    uri = github_auth.generate_oauth_redirect_uri()
    return RedirectResponse(url=uri)


@auth_router.post("/google/callback")
async def handle_google_callback(
    code: Annotated[str, Body(embed=True)],
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    tokens = await google_auth.exchange_code_for_tokens(code)
    user_info = google_auth.verify_id_token(tokens["id_token"])
    user = await google_auth.get_or_create_google_user(db, user_info)
    
    google_auth.authenticate_user(response, user.id)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "picture": user.picture,
    }


@auth_router.post("/github/callback")
async def handle_github_callback(
    code: Annotated[str, Body(embed=True)],
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    token = await github_auth.exchange_code_for_token(code)
    github_info = await github_auth.get_user_info(token)
    user = await github_auth.get_or_create_github_user(db, github_info)
    google_auth.authenticate_user(response, user.id)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "picture": user.picture,
    }


@auth_router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    user_id = google_auth.refresh_user_session(request, response)
    google_auth.set_access_token_cookie(response, user_id)
    return {"status": "refreshed"}


@auth_router.post("/logout")
async def logout(response: Response):
    google_auth.logout_user(response)
    return {"status": "logged_out"}


@auth_router.get("/profile", response_model=UserPublic)
async def get_user_data(user: CurrentUserDependency):
    return user