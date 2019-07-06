"""DataFlow URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf.urls import include, url
from .view import hello, _006650, _010060, _084990, current_time, letter, index, img_home

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^hello/$', hello),
    url(r'^index/대한유화/$', _006650),
    url(r'^index/OCI/$', _010060),
    url(r'^index/헬릭스미스/$', _084990),
    url(r'^time/$', current_time),
    url(r'^letter/$', letter),
    url(r'^index/$', index),
    url(r'^index/홈/$', img_home)


]