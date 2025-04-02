from fastapi import APIRouter, Depends, Request
import google_auth_oauthlib.flow
from config import get_settings
from .auth import GoogleOAuth

settings = get_settings()

router = APIRouter()


@router.get('/login/google')
async def google_auth():
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
    return {"authorization_url":authorization_url}


@router.get('/callback/google')
async def google_callback(request:Request):
    state = request.query_params.get("state")
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
        state=state
    )
    flow.redirect_uri = settings.AUTH_REDIRECT_URL

    authorization_response = str(request.url)
    flow.fetch_token(authorization_response=authorization_response)
    credentials = flow.credentials

    # fetch token from credentials
    token = credentials.token
    refresh_token = credentials.refresh_token
    granted_scopes= credentials.granted_scopes
    
    # fetch user information using toke
    google_auth = GoogleOAuth()
    userinfo = google_auth.get_user_info(token)

    # create user in database
    
    # create jwt token
    return {"token":"jwt token", "refresh":"refresh token"}


