import httpx

class GoogleOAuth:
    def __init__(self):
        pass

    async def get_user_info(self, token):
        user_info_url = "https://www.googleapis.com/oauth2/v3/userinfo"
        headers = {"Authorization": f"Bearer {token}"}
        async with httpx.AsyncClient() as client:
            response = await client.get(user_info_url, headers=headers, timeout=10)
            response.raise_for_status()
            return response.json()
