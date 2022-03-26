from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('reload_source_code_jstree_nodes_template', views.reload_source_code_jstree_nodes_template, name='reload_source_code_jstree_nodes_template'),
    path('projects/<path:filepath>', views.load_project, name='load_project'),
    path('load_data_frame', views.load_data_frame, name='load_data_frame'),
    path('add_new_step', views.add_new_step, name='add_new_step')
]