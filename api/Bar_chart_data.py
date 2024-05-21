import collections
from django.http import JsonResponse
from rest_framework.views import APIView
from snownlp import SnowNLP
from database import models
from database.models import Douyin
from rest_framework import serializers
from rest_framework.response import Response


class BarChartDataSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    positive_count = serializers.IntegerField()
    negative_count = serializers.IntegerField()


class BarChartData(APIView):
    def get(self, request):
        from django.db.models import Count, Case, When, IntegerField

        # 查询并计算正面情绪和负面情绪总条数
        result = Douyin.objects.values('keyword').annotate(
            positive_count=Count(Case(When(labels='正面情绪', then=1), output_field=IntegerField())),
            negative_count=Count(Case(When(labels='负面情绪', then=1), output_field=IntegerField()))
        )

        # 序列化查询结果
        serializer = BarChartDataSerializer(result, many=True)

        # 返回 JSON 格式的数据
        return Response(serializer.data)
