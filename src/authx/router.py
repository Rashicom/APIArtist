from fastapi import APIRouter, Depends, Request, HTTPException, status
import google_auth_oauthlib.flow
from config import get_settings
from .auth import GoogleOAuth, CurrentUser, create_access_token, create_refresh_token
from .schema import OAuthResponseSchema, OAuthRequestSchema
from .repository import UserRepository
from .models import User
from typing import List

settings = get_settings()

router = APIRouter()


@router.get(
  '/login/google',
  summary="login",
  description="Login with Google OAuth",
  response_model=OAuthRequestSchema
)
async def google_auth():
    auth_generator = GoogleOAuth()
    authorization_url, state = await auth_generator.get_authorization_url()
    return {"authorization_url":authorization_url}

@router.get(
  '/callback/google',
  summary="callback",
  description="Callback from Google OAuth",
  response_model=OAuthResponseSchema
)
async def google_callback(request:Request):
    state = request.query_params.get("state")
    code = request.query_params.get("code")
    # TODO: get state from redis and ensure states are matching

    google_auth = GoogleOAuth()
    credentials = await google_auth.get_tokens(code)
    
    token = credentials.get("access_token")
    refresh_token = credentials.get("refresh_token", None)
    userinfo = await google_auth.get_user_info(token)
    
    # create user in database
    user_obj = await UserRepository.get_user_by_email(userinfo.get("email"))

    if user_obj is None:
        user_obj = await UserRepository.create_user(
            email=userinfo.get("email"),
            name=userinfo.get("name"),
            google_sub_id=userinfo.get("sub"),
            token=str(token),
            refresh_token=str(refresh_token),
        )
    if user_obj is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Some error found")
    
    # create jwt token and return response
    return {"token":create_access_token(str(user_obj.id)), "refresh":create_refresh_token(str(user_obj.id))}



@router.get(
  "/me",
  response_model=User
)
async def get_me(user:CurrentUser):
    return user
