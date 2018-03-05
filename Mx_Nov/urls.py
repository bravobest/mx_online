# encoding: utf-8
"""Mx_Nov URL Configuration


The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url, include

from django.contrib import admin
import xadmin
from users.views import LoginView, index, RegisterView, ActiveUserView, ForgetPwdView, ResetPwdView, ModifyView, MyTestView
from organization.views import OrgListView

from django.views.static import serve
from settings import MEDIA_ROOT

urlpatterns = [
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^$', index, name='index'),
    url(r'^login/$', LoginView.as_view(), name='login'),
    url(r'^register/$', RegisterView.as_view(), name='register'),
    url(r'^captcha/', include('captcha.urls')),
    url(r'^active/(?P<active_code>.*)/$', ActiveUserView.as_view(), name='active_user'),
    url(r'^forget/$', ForgetPwdView.as_view(), name='forget'),
    url(r'^reset_pwd/(?P<reset_code>.*)/$', ResetPwdView.as_view(), name='reset'),
    url(r'^modify/$', ModifyView.as_view(), name='modify'),

    # 配置上传文件的访问处理函数
    url(r'^media/(?P<path>.*)', serve, {'document_root':MEDIA_ROOT}),

    # apps
    url(r'^org/', include('organization.urls', namespace='org')),
    url(r'^course/', include('courses.urls', namespace='course')),
    url(r'^user/', include('users.urls', namespace='user')),
    # test
    url(r'^test/$', MyTestView.as_view())
]
