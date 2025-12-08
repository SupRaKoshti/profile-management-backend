import time
from fastapi import Request
from app.logger import logger

async def log_requests(request: Request, call_next):
    """
    Middleware to log all requests and responses
    """
    start_time = time.time()
    
    logger.info(f"Request: {request.method} {request.url.path}")
    logger.debug(f"Headers: {dict(request.headers)}")
    
    try:
        response = await call_next(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        logger.info(
            f"Response: {request.method} {request.url.path} "
            f"Status: {response.status_code} Duration: {duration:.3f}s"
        )
        
        return response
        
    except Exception as e:
        duration = time.time() - start_time
        logger.error(
            f"Request failed: {request.method} {request.url.path} "
            f"Error: {str(e)} Duration: {duration:.3f}s",
            exc_info=True
        )
        raise