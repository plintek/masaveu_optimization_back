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
        # try:
        json_data = []
        with open("/api/utils/data.json", "r") as file:
            json_data = json.load(file)

        for i in range(len(json_data["destinations"])):
            destination = json_data["destinations"][i]
            if "id" in destination:
                del destination["id"]
            if "isNew" in destination:
                del destination["isNew"]

        for i in range(len(json_data["pexs"])):
            pex = json_data["pexs"][i]
            if "id" in pex:
                del pex["id"]
            if "isNew" in pex:
                del pex["isNew"]

        for i in range(len(json_data["orders"])):
            order = json_data["orders"][i]
            if "id" in order:
                del order["id"]
            if "isNew" in order:
                del order["isNew"]

            pex_id = json_data["orders"][i]["origin"]
            selected_pex = None
            for pex in json_data["pexs"]:
                if pex["uid"] == pex_id:
                    selected_pex = pex
                    break
            destination_id = json_data["orders"][i]["destination"]
            selected_destination = None
            for destination in json_data["destinations"]:
                if destination["uid"] == destination_id:
                    selected_destination = destination
                    break

            json_data["orders"][i]["origin"] = selected_pex
            json_data["orders"][i]["destination"] = selected_destination

        for i in range(len(json_data["vehicles"])):
            vehicle = json_data["vehicles"][i]
            if "id" in vehicle:
                del vehicle["id"]
            if "isNew" in vehicle:
                del vehicle["isNew"]

            if "geolocation_lat" in vehicle and "geolocation_lon" in vehicle:
                vehicle["geolocation"] = {
                    "lat": vehicle["geolocation_lat"],
                    "lon": vehicle["geolocation_lon"]
                }
            if "geolocation_lat" in vehicle:
                del vehicle["geolocation_lat"]
            if "geolocation_lon" in vehicle:
                del vehicle["geolocation_lon"]

            json_data["vehicles"][i] = vehicle

        data = {
            "input": request.data,
            **json_data
        }

        url = "http://host.docker.internal:5757/"

        response = requests.post(url, json=data)
        response_data = response.json()
        return Response(response_data, status=status.HTTP_200_OK)
        # except Exception as e:
        #     logger.error("Error in ExecuteAlgorithmApiView: " + str(e))
        #     return Response({"error": "Error in ExecuteAlgorithmApiView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class SaveDataApiView(APIView):

    def post(self, request):
        try:
            data = request.data
            with open("/api/utils/data.json", "w") as file:
                json.dump(data, file)

            return Response({"message": "File saved succesfully"}, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error in ExecuteAlgorithmApiView: " + str(e))
            return Response({"error": "Error in ExecuteAlgorithmApiView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class LoadDataApiView(APIView):

    def get(self, request):
        try:
            json_data = []
            with open("/api/utils/data.json", "r") as file:
                json_data = json.load(file)

            return Response(json_data, status=status.HTTP_200_OK)
        except Exception as e:
            logger.error("Error in ExecuteAlgorithmApiView: " + str(e))
            return Response({"error": "Error in ExecuteAlgorithmApiView"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
