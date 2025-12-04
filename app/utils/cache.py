import asyncio
import time
from functools import wraps


import asyncio
import time
import logging
from functools import wraps

logger = logging.getLogger("storage_cache")
logger.setLevel(logging.INFO)


def async_ttl_cache(ttl: int = 3600, max_size: int = 128):
    """
    Production-grade async TTL cache.
    - TTL expiration
    - Max size eviction
    - Logging (hit / miss / expired)
    - Safe for async functions
    """

    def decorator(func):
        cache = {}   # key → (value, timestamp)
        lock = asyncio.Lock()

        def make_key(args, kwargs):
            return (func.__name__, args, tuple(sorted(kwargs.items())))

        @wraps(func)
        async def wrapper(*args, **kwargs):
            key = make_key(args, kwargs)
            now = time.time()

            # Cache HIT
            if key in cache:
                value, timestamp = cache[key]
                if now - timestamp < ttl:
                    logger.info(f"[CACHE HIT] {func.__name__}{args} {kwargs}")
                    return value
                else:
                    logger.info(f"[CACHE EXPIRED] {func.__name__}{args} {kwargs}")
                    del cache[key]

            # Cache MISS
            logger.info(f"[CACHE MISS] {func.__name__}{args} {kwargs}")

            async with lock:
                # Double check inside lock
                if key in cache:
                    value, timestamp = cache[key]
                    if now - timestamp < ttl:
                        logger.info(f"[CACHE HIT-LOCK] {func.__name__}{args} {kwargs}")
                        return value

                # Evict if too large
                if len(cache) >= max_size:
                    evicted = next(iter(cache))
                    logger.info(f"[CACHE EVICT] Removing oldest key: {evicted}")
                    del cache[evicted]

                # Compute and store value
                value = await func(*args, **kwargs)
                cache[key] = (value, now)
                return value

        return wrapper

    return decorator