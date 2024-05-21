"""IntelligentHome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))

    选择DJ的项目进行启动程序

    http://127.0.0.1:8080/login

    超级管理员账号密码：admin   admin123

"""

from django.urls import re_path as url
from django.contrib import admin

import database.views
from api import collection, run_main, ciyun, pie, keyword, run_main2,Bar_chart_data
from page import data_page, href_index, ciyun_page, pie_page, keyword_page, ball_page,barchart_page
from . import settings
from django.views.static import serve
from database import views

urlpatterns = [

    url(r'login/', admin.site.urls),

    url(r'index', data_page.DataPage.as_view()),

    url('page/search', href_index.Index.as_view()),

    url('run/main/$', run_main.RequestsMain.as_view()),

    url('run/douyin/$', run_main2.DouyinRequests.as_view()),

    url(r'^media/(?P<path>.*)', serve, {"document_root": settings.MEDIA_ROOT}),

    url('api/collection/$', collection.Collection.as_view()),

    url(r'href/ciyun', ciyun_page.Ciyun.as_view()),
    url(r'api/ciyun', ciyun.CiYunData.as_view()),

    url(r'href/pie', pie_page.Bar.as_view()),
    url(r'api/pie', pie.ApiBar.as_view()),

    url(r'href/ball', ball_page.Ball.as_view()),

    url(r'href/keyword', keyword_page.KeyWord.as_view()),
    url(r'api/keyword', keyword.ApiKeyWord.as_view()),
    url(r'api/bardata',Bar_chart_data.BarChartData.as_view()),
    url(r'href/bar',barchart_page.BarChart.as_view()),
    url("train/", views.train)

]
