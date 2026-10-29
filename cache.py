import json
import os
from dotenv import load_dotenv
from upstash_redis import Redis

load_dotenv()

redis_url = os.getenv("UPSTASH_REDIS_REST_URL")
redis_token = os.getenv("UPSTASH_REDIS_REST_TOKEN")

if not redis_url or not redis_token:
    raise RuntimeError("Configure UPSTASH_REDIS_REST_URL e UPSTASH_REDIS_REST_TOKEN no arquivo .env.")

redis = Redis(url=redis_url, token=redis_token)

CACHE_KEY = "cinelist:movies"
CACHE_TTL = 60

def buscar_cache():
    data = redis.get(CACHE_KEY)
    if data is None:
        return None
    if isinstance(data, str):
        return json.loads(data)
    return data

def salvar_cache(filmes):
    redis.set(CACHE_KEY, json.dumps(filmes), ex=CACHE_TTL)

def limpar_cache():
    redis.delete(CACHE_KEY)
