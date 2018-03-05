# encoding: utf-8
import json
from django.shortcuts import render
from django.views.generic import View
from django.contrib.auth import authenticate, login
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from django.http import HttpResponse

from utils.email_send import send_email
from utils.mixin_utils import LoginRequiredMixin
from .forms import LoginForm, RegisterForm, ForgetPwdForm, ModifyForm, ImageUploadForm
from .models import UserProfile, EmailVerifyRecord


class MyTestView(View):
    def get(self, request):
        return render(request, 'test.html')


class CustomBackend(ModelBackend):
    def authenticate(self, username=None, password=None, **kwargs):
        try:
            user_profile = UserProfile.objects.get(Q(username=username) | Q(email=username))
            if user_profile.check_password(password):
                return user_profile
        except Exception as e:
            return None


def index(request):
    return render(request, 'index.html')


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        return render(request, 'login.html', {'login_form': login_form})

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = request.POST.get('username', '')
            password = request.POST.get('password', '')
            user = authenticate(username=username, password=password)
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return render(request, 'index.html', {'login_form': login_form})
                else:
                    return render(request, "login.html", {"msg": "用户未激活"})
            else:
                return render(request, "login.html", {"msg": "用户名密码错误"})
        else:
            return render(request, 'login.html', {'login_form': login_form})


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        return render(request, 'register.html', {'register_form': register_form})

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            user = UserProfile.objects.filter(email=email)
            if user:
                return render(request, 'register.html', {'msg': 'NO. exists', 'register_form': register_form})

            user_profile = UserProfile()
            user_profile.email = email
            user_profile.username = email
            user_profile.password = make_password(password)
            user_profile.is_active = False
            user_profile.save()
            send_email(email, 'register')
            return render(request, 'login.html')
        return render(request, 'register.html', {'register_form': register_form})


class ActiveUserView(View):
    def get(self, request, active_code):
        all_records = EmailVerifyRecord.objects.filter(code=active_code)
        if all_records:
            for record in all_records:
                email = record.email
                user = UserProfile.objects.get(email=email)
                user.is_active = True
                user.save()
                return render(request, 'login.html')
        else:
            return render(request, 'active_failed.html')


class ForgetPwdView(View):
    def get(self, request):
        forget_pwd_form = ForgetPwdForm()
        return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

    def post(self, request):
        forget_pwd_form = ForgetPwdForm(request.POST)
        if forget_pwd_form.is_valid():
            email = request.POST.get('email', '')
            all_record = UserProfile.objects.filter(email=email)
            if all_record:
                for record in all_record:
                    if record.is_active:
                        send_email(email, 'forget')
                        return render(request, 'send_success.html')
                    else:
                        return render(request, 'forgetpwd.html',
                                      {'msg': u'还没有激活过这个邮箱耶', 'forget_pwd_form': forget_pwd_form})
            else:
                return render(request, 'forgetpwd.html', {'msg': u'您还没有注册过哟', 'forget_pwd_form': forget_pwd_form})
        else:
            return render(request, 'forgetpwd.html', {'forget_pwd_form': forget_pwd_form})

            # 下面是bobby写的 感觉功能不完善
            #     send_email(email, 'forget')
            #
            #     return render(request, 'send_success.html')
            # else:
            #     return render(request, 'forgetpwd.html', {'forget_pwd_form':forget_pwd_form})


class ResetPwdView(View):
    def get(self, request, reset_code):
        # forget_pwd_form = ForgetPwdForm() 这里不用实例化这个form 因为get方法只需要展示出这个页面，还不需要填入数据
        # 也就不需要显示错误信息 比如之前的 各种form的errors，但是下面的post方法应该还是要的
        # 也不对，errors是在post方法里才需要的，这里是因为验证码没有了，所以不需要form实例了
        all_record = EmailVerifyRecord.objects.filter(code=reset_code)
        if all_record:
            for record in all_record:
                email = record.email
                return render(request, 'password_reset.html', {'email': email})
        else:
            return render(request, 'active_failed.html')


class ModifyView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            email = request.POST.get('email', '')
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            if password == password2:
                user = UserProfile.objects.get(email=email)
                user.password = make_password(password)
                user.save()
                return render(request, 'login.html')
            else:
                return render(request, 'password_reset.html', {'msg': u'两次输入不一致', 'email': email})
        else:
            email = request.POST.get('email', '')
            return render(request, 'password_reset.html', {'modify_form': modify_form, 'email': email})






# usercenter
class UserInfoView(View):
    def get(self, request):
        return render(request, 'usercenter-info.html')


class ImageUploadView(LoginRequiredMixin, View):
    def post(self, request):
        image_form = ImageUploadForm(request.POST, request.FILES, instance=request.user)
        if image_form.is_valid():
            image_form.save()
            return HttpResponse('{"status":"success"}', content_type='application/json')
        else:
            return HttpResponse('{"status":"fail"}', content_type='application/json')


class UpdatePwdView(View):
    def post(self, request):
        modify_form = ModifyForm(request.POST)
        if modify_form.is_valid():
            password = request.POST.get('password', '')
            password2 = request.POST.get('password2', '')
            if password == password2:
                user = request.user
                user.password = make_password(password)
                user.save()
                return HttpResponse('{"status": "success", "msg":"修改成功"}', content_type="application/json")
            else:
                return HttpResponse('{"status": "fail", "msg":"修改失败"}', content_type="application/json")
        else:
            return HttpResponse(json.dumps(modify_form.errors), content_type="application/json")
