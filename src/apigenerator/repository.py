from .models import Endpoints

class EndpointRepository:

    async def create(*args, **kwargs):
        try:
            endpoint_obj = Endpoints(**kwargs)
            endpoint_obj.insert()
            return endpoint_obj
        except Exception as e:
            print("cannot create endpoint : ",e)
            return None