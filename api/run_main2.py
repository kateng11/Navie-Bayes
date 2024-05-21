import requests
from django.http import JsonResponse
from rest_framework.views import APIView
from database import models
import os
import time

from utils import douyin_pro
from utils.douyin_pro import get_keypage
from utils.requests_pro import  Tieba

BASE_DIR = os.path.dirname(os.path.abspath(__file__))



class DouyinRequests(APIView):

    def post(self, request):

        keyword = request.data.get("keyword")
        page = request.data.get("page")
        message = {}
        try:
            print("爬取抖音开始")
            get_keypage(keyword,page)
            print("成功输入关键字==="+keyword)
            message['code'] = 200
            message['message'] = "OK"
            return JsonResponse(message)
        except Exception as e:
            print(e)
            message['code'] = 444
            message['message'] = "爬取异常"
            return JsonResponse(message)
