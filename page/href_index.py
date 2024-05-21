from rest_framework.views import APIView
from django.shortcuts import render


# 数据首页
class Index(APIView):
    def get(self,request):
        return render(request, "homes.html")