from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('load_data_frame', views.load_data_frame, name='load_data_frame'),
    path('add_new_step', views.add_new_step, name='add_new_step'),

]