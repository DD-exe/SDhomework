# views.py
from django.shortcuts import render, redirect, get_object_or_404
from .models import Post,Subject,Collect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator

from django.utils import timezone
import pytz

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('post_list')  # 登录成功后重定向到帖子列表
        else:
            messages.error(request, "用户名或密码错误")
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    messages.success(request, "您已成功退出登录。")
    return redirect('home')  # 退出后重定向到主页

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            try:
                user = User.objects.create_user(username=username, password=password)
                user.save()
                messages.success(request, "注册成功，请登录。")
                return redirect('login')  # 注册成功后重定向到登录页面
            except Exception as e:
                messages.error(request, "注册失败，用户名已存在或其他错误")
        else:
            messages.error(request, "两次密码输入不一致")
    return render(request, 'register.html')


def home(request):
    return render(request, 'home.html')

def post_list(request):
    subjects = Subject.objects.all()  # 获取所有主题
    selected_subject = request.GET.get('subject')  # 从查询参数中获取选中的主题

    # 根据选中的主题过滤帖子
    if selected_subject:
        posts = Post.objects.filter(subject__name=selected_subject)
    else:
        posts = Post.objects.all()  # 查询所有帖子

    paginator = Paginator(posts, 5)  # 每页显示5个帖子
    page_number = request.GET.get('page')  # 获取当前页码
    page_obj = paginator.get_page(page_number)  # 获取对应页面的帖子

    return render(request, 'post_list.html', {
        'page_obj': page_obj,
        'subjects': subjects,  # 传递主题列表
        'selected_subject': selected_subject,  # 传递选中的主题
    })

@login_required
def new_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        subject_name = request.POST.get('subject')  # 从表单获取主题
        user = request.user
        print(f"Title: '{title}', Content: '{content}', subject_name: '{subject_name}'")  # 调试输出


        if title and content:  # 确保标题和内容都不为空
            # 创建或获取主题
            subject, created = Subject.objects.get_or_create(name=subject_name)

            # 创建并保存新帖子
            post = Post(title=title, content=content, user=user, subject=subject)
            post.save()

            messages.success(request, "帖子已成功发布。")
            return redirect('post_list')  # 重定向到帖子列表
        else:
            messages.error(request, "标题和内容不能为空。")

    subjects = Subject.objects.all()  # 获取所有主题
    return render(request, 'new_post.html', {
        'user_id': request.user.id,
        'username': request.user.username,
        'subjects': subjects,
    })


@login_required
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        messages.error(request, "你没有权限删除这篇帖子。")
        return redirect('post_list')

    post.delete()
    return redirect('post_list')  # 删除后重定向到帖子列表


@login_required
def edit_post(request, post_id):
    #print("GET data:", request.GET)
    #print("POST data:", request.POST)

    post = get_object_or_404(Post, id=post_id)

    if post.user != request.user:
        messages.error(request, "你没有权限编辑这篇帖子。")
        return redirect('post_list')

    if request.method == 'POST':

        title = request.POST.get("title","").strip()
        content = request.POST.get("content","").strip()
        subject_name = request.POST.get('subject',"").strip()
        print(f"Title: '{title}', Content: '{content}', subject_name: '{subject_name}'")  # 调试输出

        if title and content and subject_name:
            post.title = title
            post.content = content

            subject, created = Subject.objects.get_or_create(name=subject_name)
            post.subject = subject

            post.updated_at = timezone.now()  # 更新帖子时间
            post.save()

            messages.success(request, "帖子已成功更新。")
            return redirect('post_list')  # 编辑成功后重定向到帖子列表
        else:
            messages.error(request, "主题不能为空")


    subjects = Subject.objects.all()
    return render(request, 'edit_post.html', {
        'post': post,
        'subjects': subjects,
    })

def post_detail(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    is_collected = Collect.objects.filter(user=request.user, post=post).exists() if request.user.is_authenticated else False
    return render(request, 'post_detail.html', {'post': post, 'is_collected': is_collected})

def collect_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    collect, created = Collect.objects.get_or_create(user=request.user, post=post)
    if created:
        # 收藏成功，做一些处理
        messages.success(request, '成功收藏该帖子！')
    else:
        # 已经收藏过，做一些处理
        messages.info(request, '你已经收藏过这个帖子。')
    return redirect('post_detail', post_id=post_id)


def remove_collect(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    collect = Collect.objects.filter(user=request.user, post=post).first()
    if collect:
        collect.delete()
        messages.success(request, '成功移除收藏！')
    return redirect('post_detail', post_id=post_id)