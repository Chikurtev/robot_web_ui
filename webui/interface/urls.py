from django.conf.urls import patterns, url

from interface import views

urlpatterns = patterns('',
    url(r'^local/', views.local, name='local'),
    url(r'^tracking/', views.tracking, name='tracking'),
    url(r'^navigation/(?P<action>\S+)/', views.navigation, name='navigation'),
    url(r'^navigation/', views.navigation, name='navigation'),
    url(r'^setup/(?P<config_name>\S+)/', views.setup, name='setup'),
    url(r'^setup/', views.setup, name='setup'),
    url(r'^speech/(?P<predefined>\S+)/', views.speech, name='speech'),
    url(r'^speech/', views.speech, name='speech'),
    url(r'^voice/(?P<predefined>\S+)/', views.voice, name='voice'),
    url(r'^voice/', views.voice, name='voice'),
    url(r'^$', views.index, name='index')
)
