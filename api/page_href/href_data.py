from rest_framework.views import APIView
from django.shortcuts import render



class data_page(APIView):
    def get(self,request):
        return render(request, "index.html")