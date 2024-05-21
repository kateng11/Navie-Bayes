import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from database import models
import os
import time
from utils.requests_pro import  Tieba

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



class RequestsMain(APIView):

    def post(self, request):

        keyword = request.data.get("keyword")
        page = request.data.get("page")

        message = {}
        try:

            tieba = Tieba(keyword,int(page))
            tieba.run()
            message['code'] = 200
            message['message'] = "OK"
            return JsonResponse(message)
        except Exception as e:
            print(e)
            message['code'] = 444
            message['message'] = "爬取异常"
            return JsonResponse(message)
