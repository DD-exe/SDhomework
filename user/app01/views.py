from django.contrib.auth.decorators import login_required
from django.db.models.functions import MD5
from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout

from app01.utils.imgcode import check_code
from io import BytesIO
from django import forms
from app01.utils import validators
from django.core.mail import send_mail


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'请输入用户名'}),

    )
    password = forms.CharField(
        max_length=120,
        required=True,
        widget=forms.PasswordInput(attrs={ 'placeholder': '请输入密码'})
    )
    imgcode = forms.CharField(
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '请输入验证码','style':"width: 125px"})
    )


class RegisterForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={'placeholder':'请输入用户名'}),
        validators=[validators.validate_username]
    )
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': '请输入邮箱'})
    )
    password = forms.CharField(
        min_length=8,
        max_length=120,
        required=True,
        widget=forms.PasswordInput(attrs={ 'placeholder': '请输入密码'}),
        validators = [validators.validate_password]
    )
    password2 = forms.CharField(
        max_length=120,
        required=True,
        widget=forms.PasswordInput(attrs={'placeholder': '请再次输入您设置的密码'})
    )

class ForgetForm(forms.Form):
    email = forms.EmailField(
        max_length=254,
        required=True,
        widget=forms.EmailInput(attrs={'placeholder': '请输入您在注册时使用的邮箱'})
    )
    imgcode = forms.CharField(
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '请输入验证码', 'style': "width: 125px"})
    )


# Create your views here.
# def my_login(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         print(username, password)
#         user = authenticate(username=username, password=password)
#
#         if user is not None:
#             login(request, user)
#             return redirect('/admin/')  #这里改成网站的首页
#         else:
#             wrongmsg = "用户名或密码错误!"
#             return render(request, 'login.html', locals())
#     return render(request, "login.html",{'form':LoginForm()})

def my_login(request):
    # if request.user.is_authenticated:
    #     return redirect('/admin/')
    if request.method == 'POST':
        remember = request.POST.get('rememberpw')
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user_code = form.cleaned_data.pop('imgcode')
            real_code = request.session.get('imgcode',"")
            if real_code == "":
                form.add_error("imgcode", "验证码已过期!")
                return render(request, 'login.html', {'form': form})
            elif real_code != user_code:
                form.add_error("imgcode", "验证码错误!")
                return render(request, 'login.html', {'form': form})
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if remember != 'true':
                    request.session.set_expiry(0)
                else:
                    request.session.set_expiry(None)
                return redirect('/admin/')  #这里改成网站的首页
            else:
                form.add_error("imgcode","用户名或密码错误!")
                return render(request, 'login.html', {'form': form})
        else:
            return render(request, 'login.html', {'form': form})
    return render(request, "login.html", {'form': LoginForm()})



def register(request):
    if request.method == 'POST':
        form = RegisterForm(data=request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error("username", "用户名已被注册过！")
                return render(request, 'register.html', {'form': form})
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error("email", "邮箱已被注册过！")
                return render(request, 'register.html', {'form': form})
            elif form.cleaned_data['password'] != form.cleaned_data['password2']:
                form.add_error("password2", "两次输入的密码不一致！")
                return render(request, 'register.html', {'form': form})
            else:
                cuser = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],email=form.cleaned_data['email'])
                cuser.save()
                return redirect('/login/')
        else:
            return render(request, 'register.html', {'form': form})
    return render(request, "register.html",{'form':RegisterForm()})

# def register(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         password2 = request.POST.get('password2')
#         if username == "":
#             msg2 = "用户名不能为空！"
#             return render(request, 'register.html', locals())
#         elif password != password2:
#             msg1 = '两次输入的密码不一样！'
#             return render(request, 'register.html', locals())
#         cuser = User.objects.create_user(username=username, password=password)
#         cuser.save()
#         return redirect('/login/')
#     return render(request, "register.html")


def forget_pw(request):
    if request.method == 'POST':
        form = ForgetForm(data=request.POST)
        if form.is_valid():
            user_code = form.cleaned_data.pop('imgcode')
            real_code = request.session.get('imgcode',"")
            if real_code == "":
                form.add_error("imgcode", "验证码已过期!")
                return render(request, 'forgetpw.html', {'form': form})
            elif real_code != user_code:
                form.add_error("imgcode", "验证码错误!")
                return render(request, 'forgetpw.html', {'form': form})
            elif not User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error("email","该邮箱不存在!")
                return render(request, 'forgetpw.html', {'form': form})

                # 这里跳转到验证码部分
        else:
            return render(request, 'forgetpw.html', {'form': form})
    return render(request, "forgetpw.html",{'form':ForgetForm()})

@login_required(login_url='/login/')
def reset_pw(request):
    return render(request, "resetpw.html")

def log_out(request):
    logout(request)
    return redirect('/login/')

def img_code(request):
    img,code_string = check_code()
    if request.session.get('imgcode'):
        del request.session['imgcode']
    request.session['imgcode'] = code_string
    request.session.set_expiry(90)
    stream = BytesIO()
    img.save(stream, 'PNG')
    return HttpResponse(stream.getvalue())

