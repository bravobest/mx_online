# encoding: utf-8
from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import View
from pure_pagination import Paginator, EmptyPage, PageNotAnInteger

from .models import Course,CourseResource
from operation.models import UserFavorite, CourseComments, UserCourse
from utils.mixin_utils import LoginRequiredMixin


class CourseListView(View):
    def get(self, request):
        all_courses = Course.objects.all().order_by('-add_time')
        hot_courses = Course.objects.all().order_by('-click_nums')[:3]
        #排序
        sort = request.GET.get('sort', '')
        if sort == 'hot':
            all_courses = Course.objects.order_by('-click_nums')
        elif sort == 'students':
            all_courses = Course.objects.order_by('-students')
        # 分页
        try:
            page = request.GET.get('page', 1)
        except PageNotAnInteger:
            page = 1

        p = Paginator(all_courses, 3, request=request)

        courses = p.page(page)

        return render(request, 'course-list.html', {
            'all_courses':courses,
            'sort':sort,
            'hot_courses': hot_courses
        })


class CourseDetailView(View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        course.click_nums += 1
        course.save()
        # fav
        fav_course = False
        fav_org = False
        if request.user.is_authenticated():
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=1):
                fav_course = True
            if UserFavorite.objects.filter(user=request.user, fav_id=course.id, fav_type=2):
                fav_org = True
        # tag
        tag = course.tag
        related_courses = []
        if tag:
            related_courses = Course.objects.filter(tag=tag)[:1]
        return render(request, 'course-detail.html', {
            'course': course,
            'related_course': related_courses,
            'fav_course': fav_course,
            'fav_org': fav_org
        })


class CourseInfoView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        # 查看user是否关联的该课程
        this_user_course = UserCourse.objects.filter(user=request.user, course=course)

        if not this_user_course:
            this_user_course = UserCourse()
            this_user_course.user = request.user
            this_user_course.course = course
            this_user_course.save()

        all_course_resources = CourseResource.objects.filter(course=course)

        # 课程推荐 学过该课程的学生 还学过哪个课程
        user_courses = UserCourse.objects.filter(course=course)
        all_user_ids = [user_course.user.id for user_course in user_courses]
        all_user_courses = UserCourse.objects.filter(user_id__in=all_user_ids)
        # 上面只是在UserCourse这个model中取得了 模型集合  下面还要转到course这个model来
        all_course_ids = [user_course.course.id for user_course in all_user_courses]
        # all_related_courses = UserCourse.objects.filter(course_id__in=all_course_ids)  这是之前的错误写法 会在产生重复的课程
        # 因为在Uercourse表中 course_id并不是不重复的，因为user_id会干扰结果  所以要选择course表来filter
        all_related_courses = Course.objects.filter(id__in=all_course_ids).order_by("-click_nums")[:3]
        return render(request, 'course-video.html', {
            'course': course,
            'all_course_resources': all_course_resources,
            'all_related_courses': all_related_courses
        })


class CourseCommentView(LoginRequiredMixin, View):
    def get(self, request, course_id):
        course = Course.objects.get(id=int(course_id))
        all_course_resources = CourseResource.objects.filter(course=course)
        all_comments = CourseComments.objects.filter(course=course)
        return render(request, 'course-comment.html', {
            'course': course,
            'all_course_resources': all_course_resources,
            'all_comments': all_comments
        })


class AddCommentView(View):
    def post(self, request):
        comment = request.POST.get('comments', '')
        course_id = request.POST.get('course_id', 0)
        course = Course.objects.get(id=course_id)
        if not request.user.is_authenticated():
            return HttpResponse('{"status":"fail", "msg":"用户未登录"}', content_type='application/json')
        if course_id > 0 and comment:
            user_comment = CourseComments()
            user_comment.user = request.user
            user_comment.course = course
            user_comment.comments = comment
            user_comment.save()
            return HttpResponse('{"status":"success", "msg":"评论成功"}', content_type='application/json')
        return HttpResponse('{"status":"fail", "msg":"评论失败"}', content_type='application/json')