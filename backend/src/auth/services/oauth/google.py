import urllib.parse
import aiohttp
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from fastapi import HTTPException, Response, Request
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from ....config import settings
from ...models import User
from ..token import create_access_token, create_refresh_token, decode_token


GOOGLE_TOKEN_URL = "https://oauth2.googleapis.com/token"
GOOGLE_AUTH_URL = "https://accounts.google.com/o/oauth2/v2/auth"


def generate_oauth_redirect_uri():
    query_params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": settings.OAUTH_GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "access_type": "offline",
        "prompt": "select_account"
    }
    query_string = urllib.parse.urlencode(query_params)
    return f'https://accounts.google.com/o/oauth2/v2/auth?{query_string}'

def get_auth_url() -> str:
    params = {
        "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
        "redirect_uri": settings.OAUTH_GOOGLE_REDIRECT_URI,
        "response_type": "code",
        "scope": "openid profile email",
        "access_type": "offline",
        "prompt": "select_account"
    }
    return f"{GOOGLE_AUTH_URL}?{urllib.parse.urlencode(params)}"


async def exchange_code_for_tokens(code: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.post(
            GOOGLE_TOKEN_URL,
            data={
                "client_id": settings.OAUTH_GOOGLE_CLIENT_ID,
                "client_secret": settings.OAUTH_GOOGLE_CLIENT_SECRET,
                "grant_type": "authorization_code",
                "redirect_uri": settings.OAUTH_GOOGLE_REDIRECT_URI,
                "code": code
            }
        ) as res:
            if res.status != 200:
                payload = await res.json()
                raise HTTPException(
                    status_code=400, 
                    detail=f"Google OAuth error: {payload.get('error_description', 'Unknown error')}"
                )
            return await res.json()


def verify_id_token(token: str) -> dict:
    try:
        id_info = id_token.verify_oauth2_token(
            token, 
            google_requests.Request(), 
            settings.OAUTH_GOOGLE_CLIENT_ID
        )
        return id_info
    except ValueError as e:
        raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")
  
  
async def get_or_create_google_user(db: AsyncSession, user_info: dict) -> User:
    google_id = user_info["sub"]
    email = user_info.get("email")
    
    result = await db.execute(
        select(User).where(User.google_id == google_id)
    )
    user = result.scalar_one_or_none()
    
    if user:
        return user

    if email:
        result = await db.execute(
            select(User).where(User.email == email)
        )
        user = result.scalar_one_or_none()

    if user:
        user.google_id = google_id
        
        if not user.picture:
            user.picture = user_info.get("picture")
            
        await db.commit()
        await db.refresh(user)
        return user
    
    user = User(
        google_id=google_id,
        email=email,
        name=user_info["name"],
        picture=user_info.get("picture"),
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    
    return user


def authenticate_user(response: Response, user_id: int):
    access_token = create_access_token(user_id)
    refresh_token = create_refresh_token(user_id)
    
    cookie_options = {
        "httponly": True,
        "secure": settings.IS_PRODUCTION,
        "samesite": "lax",
    }
    
    response.set_cookie(
        key="access_token",
        value=access_token,
        max_age=15 * 60,
        **cookie_options
    )
    
    response.set_cookie(
        key="refresh_token",
        value=refresh_token,
        max_age=30 * 24 * 60 * 60,
        **cookie_options
    )
    

def set_access_token_cookie(response: Response, user_id: int):
    token = create_access_token(user_id)
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        secure=settings.IS_PRODUCTION,
        samesite="lax",
        max_age=15 * 60
    )
    

def refresh_user_session(request: Request, response: Response) -> int:
    token = request.cookies.get("refresh_token")
    if not token:
        raise HTTPException(status_code=401, detail="Refresh token missing")
    
    try:
        payload = decode_token(token)
        if payload.get("type") != "refresh":
            raise HTTPException(status_code=401, detail="Invalid token type")
        
        return int(payload["sub"])
        
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")
    
    
def logout_user(response: Response):
    cookie_params = {"httponly": True, "samesite": "lax", "secure": settings.IS_PRODUCTION}
    response.delete_cookie("access_token", **cookie_params)
    response.delete_cookie("refresh_token", **cookie_params)