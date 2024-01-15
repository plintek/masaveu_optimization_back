from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import requests
import redis
import json
from logging import getLogger
logger = getLogger("django")


class CacheUtility:
    cache = redis.Redis(host='redis', port=6379, db=0,
                        password="masaveuRedisXXYJK")

    @staticmethod
    def read_cache(key):
        # Read the cache from redis

        try:
            json_data = json.loads(CacheUtility.cache.get(key))
            return json_data
        except:
            return CacheUtility.cache.get(key)

    @staticmethod
    def write_cache(key, value, timeout=60*60*3):
        try:
            value = json.dumps(value)
        except:
            pass

        CacheUtility.cache.set(key, value, timeout)
