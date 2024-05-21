from rest_framework.views import APIView
from django.shortcuts import render



class DataPage(APIView):

    def get(self,request):
        return render(request, "index.html")