# encoding: utf-8
__author__ = 'shawn'
__date__ = '2017/11/13 9:25'


from django.conf.urls import url
from .views import UserInfoView, ImageUploadView, UpdatePwdView

urlpatterns = [
    url(r'^info/$', UserInfoView.as_view(), name='user_info'),
    url(r'^image/upload/$', ImageUploadView.as_view(), name='image_upload'),
    url(r'^update/pwd/$', UpdatePwdView.as_view(), name='update_pwd')

]