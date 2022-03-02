from django.urls import path
from . import views

app_name="main"
urlpatterns=[
    path('',views.index,name='index'),#메인페이지
    path('login/',views.login,name='login'),#로그인,회원가입
    path('logout/',views.logout,name='logout'),#로그아웃
    path('register/',views.register,name='register'),#회원가입
]