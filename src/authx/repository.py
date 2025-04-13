from .models import User


class UserRepository:
    async def get_all_users():
        return await User.find().to_list(None)
    
    async def get_user_by_email(email):
        return await User.find_one({"email": email})
        
    async def get_user_by_id(id):
        return await User.get(id)

    async def create_user(*args, **kwargs):
        try:
            user = User(**kwargs)
            await user.insert()
            return user
        except Exception as e:
            print(f"Error creating user: {e}")
            return None