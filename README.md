# SDHomework

一个搭建Web应用的大作业。网站是信息安全综合网站。

主要实现了信安网站导航、文本和文件加解密、信安论坛等功能，并对Django内置的用户登录界面做了改进。

## 目录结构

```tree
.
├── Monaco.ttf----------------- 图形验证码字体文件
├── UserManage----------------- 用户管理模块
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── templates-------------- 用户管理模块包含的网页模板
│   │   ├── alterpw.html
│   │   ├── editpage.html
│   │   ├── favpost.html
│   │   ├── file_encoder------ 工具库模块包含的网页模板
│   │   │   ├── footer.html
│   │   │   ├── nav.html
│   │   │   ├── navbar.html
│   │   │   ├── root.html
│   │   │   └── themeToggler.html
│   │   ├── forgetpw.html
│   │   ├── login.html
│   │   ├── nav.html
│   │   ├── register.html
│   │   ├── resetpw.html
│   │   ├── usercomment.html
│   │   ├── userpage.html
│   │   ├── userpost.html
│   │   └── userreply.html
│   ├── tests.py
│   ├── urls.py---------------- 用户管理相关的url
│   ├── utils
│   │   ├── imgcode.py--------- 用于生成图形验证码
│   │   ├── randomstr.py
│   │   └── validators.py------ 网页访问者登录与否的判断与重定向
│   └── views.py--------------- 用户管理相关视图的实现
├── file_encoder--------------- 文件加密app(工具库模块)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── templates
│   │   └── file_encoder
│   │       └── index.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py--------------- 简单功能的视图实现
├── forum---------------------- 论坛app
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── serializers.py
│   ├── templates
│   │   ├── base.html
│   │   ├── edit_post.html
│   │   ├── home.html
│   │   ├── new_comment.html
│   │   ├── new_post.html
│   │   ├── new_reply.html
│   │   ├── post_detail.html
│   │   └── post_list.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py---------------- 论坛功能的视图实现
├── home ----------------------- 主页 app
├── middleware ----------------- 记录用户上一个url的中间件
│   └── session.py
├── recreate_db_site_nav.py----- 添加测试用数据
├── requirements.txt------------ python环境
├── site_nav ------------------- 网站导航app
│   ├── config.py--------------- 测试debug配置
│   ├── middleware-------------- 权限检查中间件
│   │   └── auth.py
│   ├── models.py
│   ├── templates
│   │   ├── site_add_edit.html
│   │   ├── site_list.html
│   │   ├── site_nav.html------- app主页面
│   │   └── test_login.html----- 测试用登录页面
│   ├── tests------------------- 测试用的User
│   ├── urls.py
│   └── views.py
├── templates
│   ├── footer.html------------- 页脚
│   ├── navbar.html------------- 顶部导航栏
│   ├── root.html--------------- 基础模板
│   └── theme_toggler.html------ 亮暗主题切换
├── txtencoder------------------ 文本加密app(工具库模块)
│   ├── admin.py
│   ├── apps.py
│   ├── models.py
│   ├── templates
│   │   └── txtencoder
│   │       └── index.html
│   ├── tests.py
│   ├── urls.py
│   └── views.py------------- 简单功能的视图实现
└── web_project
    ├── settings.py
    └── urls.py
```

windows生成目录结构：[tree](https://gnuwin32.sourceforge.net/packages/tree.htm)
