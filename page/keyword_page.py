from rest_framework.views import APIView
from django.shortcuts import render



class KeyWord(APIView):

    def get(self,request):
        return render(request, "keyword.html")