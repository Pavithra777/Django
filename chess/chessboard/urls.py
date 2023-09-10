from django.urls import path
from . import views

urlpatterns=[
    path('',views.home,name='home'),
    path('room/<str:game>/<str:direction>/',views.room,name='room'),
]
