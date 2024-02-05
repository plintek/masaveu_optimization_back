from rest_framework.views import APIView
from rest_framework.response import Response
import requests
import redis
import json
from logging import getLogger
from rest_framework import status, permissions
from users.authentications import CsrfExemptSessionAuthentication

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


class ExecuteAlgorithmApiView(APIView):

    def post(self, request):
        try:
            vehicles = []
            orders = []

            with open("/api/utils/orders.json", "r") as file:
                orders = json.load(file)

            with open("/api/utils/vehicles.json", "r") as file:
                vehicles = json.load(file)

            data = {
                "input": request.data,
                "orders": orders,
                "vehicles": vehicles
            }
            url = "http://host.docker.internal:5757/"

            response = requests.post(url, json=data)
            response_data = response.json()
            return Response(response_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error in ExecuteAlgorithmApiView: " + str(e))
            return Response({"error": "Error in ExecuteAlgorithmApiView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveDataApiView(APIView):

    def post(self, request):
        try:
            data = request.data
            orders = data.get("orders")
            vehicles = data.get("vehicles")
            # Check if data is valid json
            if not isinstance(orders, list) or not isinstance(vehicles, list):
                return Response({"error": "Invalid data"}, status=status.HTTP_400_BAD_REQUEST)
            with open("/api/utils/orders.json", "w") as file:
                json.dump(orders, file)

            with open("/api/utils/vehicles.json", "w") as file:
                json.dump(vehicles, file)
            return Response({"message": "File saved succesfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error in ExecuteAlgorithmApiView: " + str(e))
            return Response({"error": "Error in ExecuteAlgorithmApiView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoadDataApiView(APIView):

    def get(self, request):
        try:
            vehicles = []
            orders = []

            with open("/api/utils/orders.json", "r") as file:
                orders = json.load(file)

            with open("/api/utils/vehicles.json", "r") as file:
                vehicles = json.load(file)

            return Response({"orders": orders, "vehicles": vehicles}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error in ExecuteAlgorithmApiView: " + str(e))
            return Response({"error": "Error in ExecuteAlgorithmApiView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
