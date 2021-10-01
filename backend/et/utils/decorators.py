from functools import wraps

from fastapi.responses import JSONResponse
from loguru import logger

from et.utils.exceptions import CollectorException


def wrap_exception():
    """
    wrap exceptions so we can customize the error response usually sent by
    FastAPI that only contain 'detail' and not option for an error code
    """
    def factory(view_func):
        @wraps(view_func)
        async def decorator(*args, **kwargs):
            try:
                return await view_func(*args, **kwargs)
            except CollectorException as e:
                logger.exception(e.parent)
                logger.debug(f"[ERROR] original data was: {e.event}")

                # uvicorn forbids non-standard http response codes, so only use 400/500 for errors
                http_code = 400
                if e.status_code == 500:
                    http_code = 500

                return JSONResponse(status_code=http_code, content={
                    "code": e.status_code,
                    "detail": str(e.parent)
                })
        return decorator
    return factory
