from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_data_frame', views.load_data_frame, name='load_data_frame'),
]