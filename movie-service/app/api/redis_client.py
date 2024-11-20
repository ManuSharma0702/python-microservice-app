from redis import Redis
from fastapi import Depends

# Initialize Redis client (this could be async if needed)
redis_client = Redis(host='redis-db', db=0,socket_timeout = 5)

# Dependency to get the Redis client (for dependency injection)
def get_redis_client():
    return redis_client

