from django.urls import path
from . import views

urlpatterns=[
    path('search/',views.search,name="search"),
    path('shopping/<pk>/',views.shopping2,name="shop2"),
    path('result/',views.board_list,name="result"),
    path('pcreate/',views.p_create,name='pC'),
    path('<int:article_pk>/likes/', views.likes, name='likes'),
    path('array/',views.page_array, name="page_array"),
    path('replyC/',views.reply_create,name="rC"),
    path('<pk>/p_edit/',views.p_edit,name='p_edit'),
    path('<pk>/delete/',views.delete,name='delete'),
]