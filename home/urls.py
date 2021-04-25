from django.urls import path # path 함수를 이용하기 위해서 선언
from . import views     # 현재 폴더에 views.py를 가져옴

urlpatterns = [
    path('', views.home, name = 'home'),
    path('faq', views.faq, name = 'faq'),
]