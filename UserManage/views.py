import uuid
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.db.models.functions import MD5
from django.shortcuts import render, redirect , HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from UserManage.utils.imgcode import check_code
from io import BytesIO
from django import forms
from UserManage.utils import validators,randomstr
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
    imgcode = forms.CharField(
        max_length=5,
        required=True,
        widget=forms.TextInput(attrs={'placeholder': '请输入验证码', 'style': "width: 125px"})
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

class AlterForm(forms.Form):
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

class ResetForm(forms.Form):
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
            user_code = form.cleaned_data.pop('imgcode').lower()
            real_code = request.session.get('imgcode',"").lower()
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
                return redirect('/forum/home/')  #这里改成网站的首页
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
            user_code = form.cleaned_data.pop('imgcode').lower()
            real_code = request.session.get('imgcode', "").lower()
            if real_code == "":
                form.add_error("imgcode", "验证码已过期!")
                return render(request, 'register.html', {'form': form})
            elif real_code != user_code:
                form.add_error("imgcode", "验证码错误!")
                return render(request, 'register.html', {'form': form})
            elif User.objects.filter(username=form.cleaned_data['username']).exists():
                form.add_error("username", "用户名已被注册过！")
                return render(request, 'register.html', {'form': form})
            elif User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error("email", "邮箱已被注册过！")
                return render(request, 'register.html', {'form': form})
            elif form.cleaned_data['password'] != form.cleaned_data['password2']:
                form.add_error("password2", "两次输入的密码不一致！")
                return render(request, 'register.html', {'form': form})
            else:
                cuser = User.objects.create_user(username=form.cleaned_data['username'], password=form.cleaned_data['password'],email=form.cleaned_data['email'],is_active=False)
                cuser.save()
                # 使用uuid产生一个token
                token = str(uuid.uuid4()).replace('-', '')
                # 使用session存储token
                request.session[token] = form.cleaned_data['username']
                request.session.save()  # 保存session到数据库或缓存
                request.session.set_expiry(60 * 60 * 24)
                username = User.objects.get(email=form.cleaned_data['email']).username
                subject = "信安综合网站账号激活邮件"
                path = f'http://127.0.0.1:8000/active?token={token}'  # 这里记得要改成最终公网地址
                message = f"""
                                                <html>
                                                    <head>
                                                        <style>
                                                            body {{
                                                                font-family: Arial, sans-serif;
                                                                background-color: #f2f2f2;
                                                            }}

                                                            .container {{
                                                                position: relative;
                                                                max-width: 600px;
                                                                margin: 0 auto;
                                                                padding: 20px;
                                                                background-color: #fff;
                                                                border-radius: 5px;
                                                                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                                            }}

                                                            h1 {{
                                                                color: #333;
                                                                font-size: 24px;
                                                                margin-bottom: 20px;
                                                            }}

                                                            p {{
                                                                color: #555;
                                                                font-size: 16px;
                                                                line-height: 1.5;
                                                            }}

                                                            a {{
                                                                color: #007bff;
                                                                text-decoration: none;
                                                            }}

                                                            a:hover {{
                                                                text-decoration: underline;
                                                            }}

                                                            p.signature {{
                                                                position: absolute;
                                                                bottom: 10px;
                                                                right: 30px;
                                                                color: #555;
                                                                font-size: 16px;
                                                                line-height: 1.5;
                                                            }}
                                                        </style>
                                                    </head>
                                                    <body>
                                                        <div class="container">
                                                            <p>尊敬的用户{username}您好：
                                                            <p>您刚刚进行了账号注册的申请，请点击下面链接激活您的账号：</p>
                                                            <p><a href="http://127.0.0.1:8000/active?token={token}">点击激活账号</a></p>
                                                            <p>如果链接不可用，请复制以下内容到浏览器打开：</p>
                                                            <p>{path}</p>
                                                            <p>链接有效期为24小时，请及时处理。若您忘记用户名，可见上方的邮件称呼。</p>
                                                            <p>若您并未在此网站注册账号，切勿点击上方链接</p>
                                                            <br>
                                                            <br>
                                                            <p class="signature">信安综合网站NISWEB</p>
                                                        </div>
                                                    </body>
                                                </html>
                                                """
                send_status = send_mail(subject=subject, message='', html_message=message,
                                        from_email=settings.EMAIL_HOST_USER,
                                        recipient_list=[form.cleaned_data['email']])
                if send_status:
                    msg = "账号激活邮件已发送至您的邮箱，邮件有效期为24小时，请尽快查收并进行下一步操作！"
                else:
                    msg = "账号激活邮件发送失败，请稍后再试"
                messages.success(request, msg)
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
            user_code = form.cleaned_data.pop('imgcode').lower()
            real_code = request.session.get('imgcode',"").lower()
            if real_code == "":
                form.add_error("imgcode", "验证码已过期!")
                return render(request, 'forgetpw.html', {'form': form})
            elif real_code != user_code:
                form.add_error("imgcode", "验证码错误!")
                return render(request, 'forgetpw.html', {'form': form})
            elif not User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error("email","该邮箱不存在!")
                return render(request, 'forgetpw.html', {'form': form})
            else:
                # 使用uuid产生一个token
                token = str(uuid.uuid4()).replace('-', '')
                # 使用session存储token
                request.session[token] = form.cleaned_data['email']
                #request.session[str(token)] = form.cleaned_data['email']
                request.session.save()  # 保存session到数据库或缓存
                #request.session['forget_email'] = form.cleaned_data['email']
                request.session.set_expiry(60*60*24)
                username = User.objects.get(email=form.cleaned_data['email']).username
                subject = "信安综合网站密码找回邮件"
                path = f'http://127.0.0.1:8000/reset?token={token}'  # 这里记得要改地址
                code = randomstr.random_str()
                #message = f"验证码为：{code}"
                message = f"""
                                <html>
                                    <head>
                                        <style>
                                            body {{
                                                font-family: Arial, sans-serif;
                                                background-color: #f2f2f2;
                                            }}

                                            .container {{
                                                position: relative;
                                                max-width: 600px;
                                                margin: 0 auto;
                                                padding: 20px;
                                                background-color: #fff;
                                                border-radius: 5px;
                                                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                            }}

                                            h1 {{
                                                color: #333;
                                                font-size: 24px;
                                                margin-bottom: 20px;
                                            }}

                                            p {{
                                                color: #555;
                                                font-size: 16px;
                                                line-height: 1.5;
                                            }}

                                            a {{
                                                color: #007bff;
                                                text-decoration: none;
                                            }}

                                            a:hover {{
                                                text-decoration: underline;
                                            }}

                                            p.signature {{
                                                position: absolute;
                                                bottom: 10px;
                                                right: 30px;
                                                color: #555;
                                                font-size: 16px;
                                                line-height: 1.5;
                                            }}
                                        </style>
                                    </head>
                                    <body>
                                        <div class="container">
                                            <p>尊敬的用户{username}您好：
                                            <p>您刚刚进行了密码找回的申请，请点击下面链接重置您的账号密码以完成密码找回：</p>
                                            <p><a href="http://127.0.0.1:8000/reset?token={token}">点击重置密码</a></p>
                                            <p>如果链接不可用，请复制以下内容到浏览器打开：</p>
                                            <p>{path}</p>
                                            <p>链接有效期为24小时，请及时处理。若您忘记用户名，可见上方的邮件称呼。</p>
                                            <p>若您并未进行找回密码的操作，切勿点击上方链接</p>
                                            <br>
                                            <br>
                                            <p class="signature">信安综合网站NISWEB</p>
                                        </div>
                                    </body>
                                </html>
                                """
                send_status = send_mail(subject=subject, message='',html_message=message,from_email=settings.EMAIL_HOST_USER,recipient_list=[form.cleaned_data['email']])
                if send_status:
                    msg = "找回邮件已发送至您的邮箱，邮件有效期为24小时，请尽快查收并进行下一步操作！"
                else:
                    msg = "邮件发送失败，请稍后再试"
                messages.success(request, msg)
                return redirect('/login/')

        else:
            return render(request, 'forgetpw.html', {'form': form})
    return render(request, "forgetpw.html",{'form':ForgetForm()})

def alter_pw(request):
    if request.method == 'POST':
        form = AlterForm(data=request.POST)
        if form.is_valid():
            user_code = form.cleaned_data.pop('imgcode').lower()
            real_code = request.session.get('imgcode',"").lower()
            if real_code == "":
                form.add_error("imgcode", "验证码已过期!")
                return render(request, 'alterpw.html', {'form': form})
            elif real_code != user_code:
                form.add_error("imgcode", "验证码错误!")
                return render(request, 'alterpw.html', {'form': form})
            elif not User.objects.filter(email=form.cleaned_data['email']).exists():
                form.add_error("email","该邮箱不存在!")
                return render(request, 'alterpw.html', {'form': form})
            else:
                # 使用uuid产生一个token
                token = str(uuid.uuid4()).replace('-', '')
                # 使用session存储token
                request.session[token] = form.cleaned_data['email']
                request.session.save()  # 保存session到数据库或缓存
                request.session.set_expiry(60*60*24)
                username = User.objects.get(email=form.cleaned_data['email']).username
                subject = "信安综合网站密码更改邮件"
                path = f'http://127.0.0.1:8000/reset?token={token}'  # 这里记得要改地址
                message = f"""
                                <html>
                                    <head>
                                        <style>
                                            body {{
                                                font-family: Arial, sans-serif;
                                                background-color: #f2f2f2;
                                            }}

                                            .container {{
                                                position: relative;
                                                max-width: 600px;
                                                margin: 0 auto;
                                                padding: 20px;
                                                background-color: #fff;
                                                border-radius: 5px;
                                                box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                                            }}

                                            h1 {{
                                                color: #333;
                                                font-size: 24px;
                                                margin-bottom: 20px;
                                            }}

                                            p {{
                                                color: #555;
                                                font-size: 16px;
                                                line-height: 1.5;
                                            }}

                                            a {{
                                                color: #007bff;
                                                text-decoration: none;
                                            }}

                                            a:hover {{
                                                text-decoration: underline;
                                            }}

                                            p.signature {{
                                                position: absolute;
                                                bottom: 10px;
                                                right: 30px;
                                                color: #555;
                                                font-size: 16px;
                                                line-height: 1.5;
                                            }}
                                        </style>
                                    </head>
                                    <body>
                                        <div class="container">
                                            <p>尊敬的用户{username}您好：
                                            <p>您刚刚进行了密码更改的申请，请点击下面链接修改您的账号密码：</p>
                                            <p><a href="http://127.0.0.1:8000/reset?token={token}">点击修改密码</a></p>
                                            <p>如果链接不可用，请复制以下内容到浏览器打开：</p>
                                            <p>{path}</p>
                                            <p>链接有效期为24小时，请及时处理。若您忘记用户名，可见上方的邮件称呼。</p>
                                            <p>若您并未进行更改密码的操作，切勿点击上方链接</p>
                                            <br>
                                            <br>
                                            <p class="signature">信安综合网站NISWEB</p>
                                        </div>
                                    </body>
                                </html>
                                """
                send_status = send_mail(subject=subject, message='',html_message=message,from_email=settings.EMAIL_HOST_USER,recipient_list=[form.cleaned_data['email']])
                if send_status:
                    msg = "密码更改邮件已发送至您的邮箱，邮件有效期为24小时，请尽快查收并进行下一步操作！"
                else:
                    msg = "邮件发送失败，请稍后再试"
                messages.success(request, msg)
                return redirect('/login/')

        else:
            return render(request, 'alterpw.html', {'form': form})
    return render(request, "alterpw.html",{'form':AlterForm()})

# @login_required(login_url='/login/')
def reset_pw(request):
    if request.method == 'POST':
        form = ResetForm(data=request.POST)
        if form.is_valid():
            if form.cleaned_data['password'] != form.cleaned_data['password2']:
                form.add_error("password2", "两次输入的密码不一致！")
                return render(request, 'resetpw.html', {'form': form})
            elif request.session.get('email') is None:
                form.add_error("password2", "申请有效期已过，请回到原界面重头进行操作！")
                return render(request, 'resetpw.html', {'form': form})
            else:
                email = request.session.get('email')
                del request.session['email']
                user = User.objects.get(email = email)

                user.set_password(form.cleaned_data['password'])
                user.save()
                messages.success(request, "密码修改成功，请重新登录！")
                return redirect('/login/')
        else:
            return render(request, 'resetpw.html', {'form': form})
    return render(request, "resetpw.html", {'form': ResetForm()})

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


def account_activate(request):
    token = request.GET.get('token')
    username = request.session.get(token)
    if username is None:
        messages.success(request, "链接已失效，请重新操作！")
        return redirect('/login/')
    del request.session[token]
    user = User.objects.get(username=username)
    user.is_active = True
    user.save()
    messages.success(request, "账号已激活，请进行登录！")
    return redirect('/login/')

def password_reset(request):
    token = request.GET.get('token')
    email = request.session.get(token)
    if email is None:
        messages.success(request, "链接已失效，请重新操作！")
        return redirect('/login/')
    del request.session[token]
    request.session['email'] = email
    request.session.save()
    request.session.set_expiry(60*60)
    return redirect('/resetpw/')

