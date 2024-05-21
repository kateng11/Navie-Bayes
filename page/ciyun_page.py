from rest_framework.views import APIView
from django.shortcuts import render



class Ciyun(APIView):

    def get(self,request):
        return render(request, "ciyun.html")