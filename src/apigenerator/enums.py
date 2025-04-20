from enum import StrEnum

class EndpointTypes(StrEnum):
    STATIC = "static"
    DYNAMIC = "dynamic"


class HttpMethods(StrEnum):
    GET = "GET"
    POST = "POST"
    PATCH = "PATCH"
    PUT = "PUT"
    DELETE = "DELETE"