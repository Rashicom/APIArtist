from pydantic import BaseModel, Field, EmailStr


class OAuthRequestSchema(BaseModel):
    authorization_url: str

class OAuthResponseSchema(BaseModel):
    token: str
    refresh: str

class UserResponseSchema(BaseModel):
    """
    User response schema by excluding sensitive information such as tokens
    """
    id: str
    email: EmailStr
    name: str