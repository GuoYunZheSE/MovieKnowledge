# @Date    : 13:30 01/28/2022
# @Author  : ClassicalPi
# @FileName: urls.py
# @Software: PyCharm

from django.urls import path
from rest_framework import routers
from .views import *

router=routers.DefaultRouter()

urlpatterns=[
    path('Answer/',Answer.as_view(),name="Answer"),
    path("QueryActor/",QueryActor.as_view(),name="QueryActor"),
    path("QueryMovie/",QueryMovie.as_view(),name="QueryMovie")
]
urlpatterns += router.urls