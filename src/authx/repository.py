from .models import User


class UserRepository:
    async def get_all_users():
        return await User.find().to_list(None)