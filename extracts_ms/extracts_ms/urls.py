from django.conf.urls import url
from generator import views

urlpatterns = [
    url(r'^files/', views.archivos_list),
    url(r'^file/(?P<pk>[0-9]+)/$', views.id_list),
    url(r'^generate_all/(?P<pk>[0-9]+)/$', views.extracts_all),
    url(r'^generate_days/(?P<pk>[0-9]+)/(?P<pk2>[0-9]+)/$', views.extracts_days),
]
