from django.urls import path
from . import views

urlpatterns=[
    path('search/',views.search,name="search"),
    path('shopping/<pk>/',views.shopping2,name="shop2"),
    path('pcreate/',views.p_create,name='pC'),
    path('delete/',views.delete,name='delete'),
    path('<int:article_pk>/likes/', views.likes, name='likes'),
]