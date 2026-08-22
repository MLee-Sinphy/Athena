import logging
import time
from uuid import UUID, uuid4

from django.conf import settings
from django.http import HttpResponse

request_logger = logging.getLogger("athena.request")


class RequestContextMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        supplied = request.headers.get("X-Request-ID", "")
        try:
            request_id = str(UUID(supplied))
        except (ValueError, AttributeError):
            request_id = str(uuid4())
        request.request_id = request_id
        started = time.monotonic()
        response = self.get_response(request)
        response["X-Request-ID"] = request_id
        request_logger.info(
            "request_completed",
            extra={
                "request_id": request_id,
                "method": request.method,
                "path": request.path,
                "status": response.status_code,
                "duration_ms": round((time.monotonic() - started) * 1000, 2),
            },
        )
        return response


class RestrictedCorsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        origin = request.headers.get("Origin")
        if request.method == "OPTIONS" and origin in settings.CORS_ALLOWED_ORIGINS:
            response = HttpResponse(status=204)
        else:
            response = self.get_response(request)

        if origin in settings.CORS_ALLOWED_ORIGINS:
            response["Access-Control-Allow-Origin"] = origin
            response["Access-Control-Allow-Headers"] = "Authorization, Content-Type"
            response["Access-Control-Allow-Methods"] = "GET, POST, PATCH, OPTIONS"
            response["Vary"] = "Origin"
        return response
