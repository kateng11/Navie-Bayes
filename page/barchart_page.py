from rest_framework.views import APIView
from django.shortcuts import render


class BarChart(APIView):

    def get(self, request):
        return render(request, "bar.html")
