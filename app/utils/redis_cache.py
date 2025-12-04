import json
import asyncio
import time
import logging
from redis.asyncio import Redis

logger = logging.getLogger("redis_cache")
logger.setLevel(logging.INFO)

redis = Redis(host="localhost", port=6379, decode_responses=True)


async def redis_cache_get(key: str):
    val = await redis.get(key)
    if val is None:
        return None
    logger.info(f"[REDIS HIT] {key}")
    return json.loads(val)


async def redis_cache_set(key: str, value, ttl: int):
    logger.info(f"[REDIS SET] {key} ttl={ttl}")
    await redis.set(key, json.dumps(value), ex=ttl)
