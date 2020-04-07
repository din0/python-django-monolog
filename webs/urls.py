from django.contrib import admin
from django.urls import path, re_path
from personal import views

# from . import views
#。是指从当前的目录中导入views

urlpatterns = [
    path('admin/', admin.site.urls),
    path(r'', views.index, name='index'),
    path('topics/', views.topics, name='topics'),

    re_path(r'^topics/(?P<topic_id>\d+)/$', views.topic, name='topic'),
    path('new_topic/', views.new_topic, name='new_topic'),
]
