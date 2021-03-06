from http import HTTPStatus

from sanic.request import Request
from sanic.response import BaseHTTPResponse, json

from configs.config import ApplicationConfig
from context import Context


class SanicEndpoint:

    async def __call__(self, *args, **kwargs) -> BaseHTTPResponse:
        return await self.handler(*args, **kwargs)

    def __init__(self, config: ApplicationConfig, context: Context,  uri: str, methods: list, *args, **kwargs):
        self.config = config
        self.uri = uri
        self.methods = methods
        self.context = context
        self.__name__ = self.__class__.__name__


    @staticmethod
    async def make_response_json(
            body: dict = None, status: int = 200, message: str = None, error_code: int = None
    ) -> BaseHTTPResponse:

        if body is None:
            body = {
                'message': message or HTTPStatus(status).phrase,
                'error_code': error_code or status,
            }
        return json(body=body, status=status)

    @staticmethod
    def import_body_json(request: Request) -> dict:
        if 'application/json' in request.content_type and request.json is not None:
            return dict(request.json)
        return {}

    @staticmethod
    def import_body_header(request: Request) -> dict:
        headers = {
            header: request.headers[header]
            for header in request.headers
            if header.lower().startswith('x-')
        }
        return headers

    async def handler(self, request: Request, *args, **kwargs) -> BaseHTTPResponse:
        body = {}

        body.update(self.import_body_json(request))
        body.update(self.import_body_header(request))

        return await self._method(request, body, *args, **kwargs)

    async def _method(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        method = request.method.lower()
        func_name = f'method_{method}'

        if hasattr(self, func_name):
            func = getattr(self, func_name)
            return await func(request, body, *args, **kwargs)
        return await self.method_not_impl(method=method)

    async def method_not_impl(self, method: str) -> BaseHTTPResponse:
        return await self.make_response_json(status=500, message=f'Method {method.upper()} not implemented')

    async def method_get(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='get')

    async def method_post(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='post')

    async def method_patch(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='patch')

    async def method_delete(self, request: Request, body: dict, *args, **kwargs) -> BaseHTTPResponse:
        return await self.method_not_impl(method='delete')
