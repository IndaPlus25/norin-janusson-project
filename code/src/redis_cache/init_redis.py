from redis import Redis
from config import REDIS_URL

redis_client = Redis.from_url(REDIS_URL, decode_responses=True)
