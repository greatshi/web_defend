"""web_defend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.contrib import admin
from trusted_page import views
from web_server import views as views_2
from web_miner import views as views_3
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^trusted_page/', views.trusted_page),
    url(r'^data/$', views.data),
    url(r'^web_server/web_01$', views_2.web_01),
    url(r'^web_server/web_02$', views_2.web_02),
    url(r'^miner/$', views_3.miner),
    url(r'^miner/(.{65})$', views_3.block_search),
]
