from redis import Redis
from config import REDIS_HOST, REDIS_PORT

redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, decode_responses=True)
