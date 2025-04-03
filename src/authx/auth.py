import httpx
from config import get_settings
import jwt
from datetime import datetime, timedelta, timezone
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi import Depends, HTTPException, status
from typing import Annotated
from .repository import UserRepository
from .models import User
import google_auth_oauthlib.flow


settings = get_settings()
auth2_schema = HTTPBearer()

def create_access_token(id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.JWT_EXPIRY_MINUTE)
    to_encode = {
        "id": id,
        "exp":expire
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_HASH_ALGORITHM)
    return encoded_jwt

def create_refresh_token(id: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.REFRESH_JWT_EXPIRY_MINUTE)
    to_encode = {
        "id": id,
        "exp": expire
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.JWT_HASH_ALGORITHM)
    return encoded_jwt


async def get_authenticated_user(token:HTTPAuthorizationCredentials=Depends(auth2_schema)):
    try:
        payload = jwt.decode(
            token.credentials,
            settings.SECRET_KEY,
            algorithms=[settings.JWT_HASH_ALGORITHM]
        )
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials")

    # check the token is expired or not
    if datetime.fromtimestamp(payload.get("exp"), timezone.utc) < datetime.now(timezone.utc):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Token expired")

    user_id = payload.get("id")
    user_obj = await UserRepository.get_user_by_id(user_id)
    if not user_obj:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user_obj

CurrentUser = Annotated[User, Depends(get_authenticated_user)]



class GoogleOAuth:
    def __init__(self):
        pass

    async def get_authorization_url(self):
        flow = google_auth_oauthlib.flow.Flow.from_client_config(
        {
          "web": {
            "client_id": settings.CLIENT_ID,
            "project_id": settings.PROJECT_ID,
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_secret": settings.CLIENT_SECRET
          }
        },
        scopes=["openid", "https://www.googleapis.com/auth/userinfo.email"],
        )
        flow.redirect_uri = settings.AUTH_REDIRECT_URL

        authorization_url, state = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true'
        )
        return authorization_url, state
    
    async def get_tokens(self, code):
        google_token_url = "https://oauth2.googleapis.com/token"
        data = {
            "code": code,
            "client_id": settings.CLIENT_ID,
            "client_secret": settings.CLIENT_SECRET,
            "redirect_uri": settings.AUTH_REDIRECT_URL,
            "grant_type": "authorization_code"
        }
        async with httpx.AsyncClient() as client:
            response = await client.post(google_token_url, json=data)
            response.raise_for_status()
            return response.json()
    

    async def get_user_info(self, token):
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()



