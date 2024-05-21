from rest_framework.views import APIView
from django.shortcuts import render



class Bar(APIView):

    def get(self,request):
        return render(request, "pie.html")