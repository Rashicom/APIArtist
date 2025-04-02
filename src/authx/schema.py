from pydantic import BaseModel, Field


class OAuthRequestSchema(BaseModel):
    authorization_url: str

class OAuthResponseSchema(BaseModel):
    token: str
    refresh: str