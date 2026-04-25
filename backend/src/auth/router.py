from typing import Annotated

from fastapi import APIRouter, Body, Depends, Response, Request
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

from ..database import get_db
from .services.auth import *


auth_router = APIRouter(prefix='/auth')


@auth_router.get("/google/url")
def get_google_auth_url():
    uri = generate_google_oauth_redirect_uri()
    return RedirectResponse(url=uri)


@auth_router.post("/google/callback")
async def handle_google_callback(
    code: Annotated[str, Body(embed=True)],
    response: Response,
    db: AsyncSession = Depends(get_db)
):
    tokens = await exchange_code_for_tokens(code)
    user_info = verify_id_token(tokens["id_token"])
    user = await get_or_create_google_user(db, user_info)
    
    authenticate_user(response, user.id)

    return {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "picture": user.picture,
    }


@auth_router.post("/refresh")
async def refresh_token(request: Request, response: Response):
    user_id = refresh_user_session(request, response)
    set_access_token_cookie(response, user_id)
    return {"status": "refreshed"}


@auth_router.post("/logout")
async def logout(response: Response):
    logout_user(response)
    return {"status": "logged_out"}
