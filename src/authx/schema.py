from pydantic import BaseModel, Field, EmailStr


class OAuthRequestSchema(BaseModel):
    authorization_url: str


class OAuthResponseSchema(BaseModel):
    token: str
    refresh: str
