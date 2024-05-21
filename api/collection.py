import random

from django.http import JsonResponse, HttpResponse
from rest_framework.views import  APIView
from lxml import etree
from database import models


class Collection(APIView):

    def get(self, request):


        name = request.GET.get("name")
        urls = request.GET.get("url")

        message = {}
        try:

            models.Colect.objects.create(co_title=name,co_down_link=urls)
            return HttpResponse("收藏成功")

        except Exception as e:
            print(e)
            return HttpResponse("收藏失败")