"""
URL configuration for yanbao_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from appaccounts.views import AccountView, AccountViewDetail, LogView, DanmuView
from apptools.views import FfmpegAudioSplitView 
from appmodels.views_tts_chatopenai import BigmodelsTtsChatopenaiView
from appmodels.views_tts_azure import BigmodelsTtsAzureView
from appmodels.views_tts_edge import BigmodelsTtsEdgeView
from appmodels.views_tts_baidu import BigmodelsTtsBaiduView
from appmodels.views_tts_ali import BigmodelsTtsAliView


urlpatterns = [
    path("admin/", admin.site.urls),
    path('token', obtain_auth_token),
    path('v1/account', AccountView.as_view()),
    path('v1/account/<int:id>', AccountViewDetail.as_view()),
    path('v1/log', LogView.as_view()),
    path('v1/danmu', DanmuView.as_view()),
    path('v1/ffmpeg/audio/split', FfmpegAudioSplitView.as_view()),
    path('v1/model/tts/chatopenai', BigmodelsTtsChatopenaiView.as_view()),
    path('v1/model/tts/azure', BigmodelsTtsAzureView.as_view()),
    path('v1/model/tts/edge', BigmodelsTtsEdgeView.as_view()),
    path('v1/model/tts/baidu', BigmodelsTtsBaiduView.as_view()),
    path('v1/model/tts/ali', BigmodelsTtsAliView.as_view()),
]
