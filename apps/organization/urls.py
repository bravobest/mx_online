# encoding: utf-8
__author__ = 'shawn'
__date__ = '2017/11/7 20:30'

from django.conf.urls import url
from organization.views import OrgListView, OrgHomeView, OrgCourseView, OrgDescView, OrgTeacherView, UserAskView, AddFavView

urlpatterns = [
    # 课程机构 organization
    url(r'^list/$', OrgListView.as_view(), name='org_list'),
    url(r'^home/(?P<org_id>\d+)/$', OrgHomeView.as_view(), name='org_home'),
    url(r'^course/(?P<org_id>\d+)/$', OrgCourseView.as_view(), name='org_course'),
    url(r'^desc/(?P<org_id>\d+)/$', OrgDescView.as_view(), name='org_desc'),
    url(r'^teacher/(?P<org_id>\d+)/$', OrgTeacherView.as_view(), name='org_teacher'),
    url(r'^user_ask/$', UserAskView.as_view(), name='user_ask'),
    # 机构的收藏
    url(r'^add_fav/$', AddFavView.as_view(), name='add_fav')

]
