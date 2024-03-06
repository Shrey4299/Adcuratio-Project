from fastapi import Request


class RequestLoggerMiddleware:
    def __init__(self, app):
        self.app = app

    async def __call__(self, request: Request, call_next):
        # Log the incoming request
        print(f"Incoming request: {request.method} {request.url}")

        # Call the next middleware in the chain or the request handler
        response = await call_next(request)

        return response
