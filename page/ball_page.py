from rest_framework.views import APIView
from django.shortcuts import render



class Ball(APIView):

    def get(self,request):
        return render(request, "ball.html")