#!/usr/bin/env python

# usage: 
#   1. activate python environment
#   2. just run `python recreate_db_site_nav.py`

# reference: https://docs.djangoproject.com/en/5.1/topics/settings/#calling-django-setup-is-required-for-standalone-django-usage

import os
import sys


def insert(model_index, user, data):
    from site_nav import views, models
    form = views.SiteCategoryForm(user=user, data=data) if not model_index else views.SiteNavForm(user=user, data=data)
    query = models.SiteCategory.objects.filter(**data) if not model_index else models.SiteNav.objects.filter(**data)
    if form.is_valid():
        form.save()
    elif not query.exists():
        print("Fail: ", form.errors, "; model =", model_index, " user =", user, " data =", data)
    
    return models.SiteCategory.objects.get(**data) if not model_index else None


def main():
    """Run administrative tasks."""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "web_project.settings")
    
    import django
    from django.conf import settings
    from web_project import settings as mysettings

    django.setup()

    try:
        from django.contrib.auth.models import User
        from site_nav import views, models
    except ImportError as exc:
        raise ImportError(
                "Couldn't import Django. Are you sure it's installed and "
                "available on your PYTHONPATH environment variable? Did you "
                "forget to activate a virtual environment?"
                "\nOr did you forget to add django.contrib.auth?"
                ) from exc

    spuser = None
    staff = None
    snuser = None
    if (not User.objects.filter(username="super").exists()):
        print("creating superuser \"super\"")
        spuser = User.objects.create_user(username="super", password="super", is_superuser=True, is_staff=True)
    else:
        spuser = User.objects.get(username="super")
    if (not User.objects.filter(username="staff").exists()):
        print("creating staffuser \"staff\"")
        staff = User.objects.create_user(username="staff", password="staff", is_staff=True)
    else:
        staff = User.objects.get(username="staff")
    if (not User.objects.filter(username="site_nav").exists()):
        print("creating normal user \"site_nav\"")
        snuser = User.objects.create_user(username="site_nav", password="site_nav")
    else:
        snuser = User.objects.get(username="site_nav")

    print("name\tis_superuser\tis_staff")
    for user in User.objects.all():
        print(user.username, " ", user.is_superuser, " ", user.is_staff)
    print('')

    # insert SiteCategory
    spuser1 = insert(0, spuser, {"user": spuser.id, "name": f"{spuser.username}1", "weight": 2, "description": f"{spuser.username}1, 2"})
    # spuser2 = insert(0, spuser, {"user": spuser.id, "name": f"{spuser.username}2", "weight": 3, "description": f"{spuser.username}2, 3"})
    staff1 = insert(0, staff, {"user": staff.id, "name": f"{staff.username}1", "weight": 3, "description": f"{staff.username}1, 3"})
    staff2 = insert(0, staff, {"user": staff.id, "name": f"{staff.username}2", "weight": 4, "description": f"{staff.username}2, 4"})
    snuser1 = insert(0, snuser, {"user": snuser.id, "name": f"{snuser.username}1", "weight": 4, "description": f"{snuser.username}1, 4"})
    snuser2 = insert(0, snuser, {"user": snuser.id, "name": f"{snuser.username}2", "weight": 5, "description": f"{snuser.username}2, 5"})

    print('')
    print(models.SiteCategory.fields_to_use())
    for obj in models.SiteCategory.objects.all():
        print(list(obj.fields2dict().values()))


    # insert SiteNav
    insert(1, spuser, {"user": spuser.id, "category": spuser1, "url": "https://code.visualstudio.com/", "weight": spuser1.weight + spuser.id, "description": "1"})
    insert(1, staff, {"user": staff.id, "category": staff1, "url": "https://www.sjtu.edu.cn/", "weight": staff1.weight + staff.id, "description": "2"})
    insert(1, staff, {"user": staff.id, "category": staff1, "url": "https://www.huaweicloud.com/", "weight": staff1.weight + staff.id + 1, "description": "3"})
    insert(1, staff, {"user": staff.id, "category": staff2, "url": "https://forum.butian.net/", "weight": staff2.weight + staff.id + 2, "description": "4"})
    insert(1, staff, {"user": staff.id, "category": staff2, "url": "https://www.t00ls.com/", "weight": staff2.weight + staff.id + 3, "description": "5"})
    insert(1, staff, {"user": staff.id, "category": staff2, "url": "https://stack.chaitin.com/", "weight": staff2.weight + staff.id + 4, "description": "6"})
    insert(1, staff, {"user": staff.id, "category": staff2, "url": "https://bbs.ichunqiu.com/portal.php", "weight": staff2.weight + staff.id + 5, "description": "7"})
    insert(1, staff, {"user": staff.id, "category": staff1, "url": "https://xz.aliyun.com/", "weight": staff1.weight + staff.id + 6, "description": "8"})
    insert(1, staff, {"user": staff.id, "category": staff1, "url": "https://www.freebuf.com/", "weight": staff1.weight + staff.id + 7, "description": "9"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://www.bugbank.cn/", "weight": snuser1.weight + snuser.id, "description": "10"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://www.51cto.com/netsecurity", "weight": snuser1.weight + snuser.id + 1, "description": "11"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://www.secpulse.com/", "weight": snuser1.weight + snuser.id + 2, "description": "12"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://paper.seebug.org/", "weight": snuser1.weight + snuser.id + 3, "description": "13"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "https://attack.mitre.org/", "weight": snuser2.weight + snuser.id, "description": "14"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "http://www.52bug.cn/", "weight": snuser2.weight + snuser.id + 1, "description": "15"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "https://forum.ywhack.com/", "weight": snuser2.weight + snuser.id + 2, "description": "16"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "https://govuln.com/news/", "weight": snuser2.weight + snuser.id + 3, "description": "17"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "https://forum.90sec.com/", "weight": staff2.weight + snuser.id + 4, "description": "18"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://sbbbb.cn/", "weight": staff1.weight + snuser.id + 5, "description": "19"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://portswigger.net/burp", "weight": staff1.weight + snuser.id + 5, "description": "20"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "https://www.wireshark.org/", "weight": staff2.weight + snuser.id + 4, "description": "21"})
    insert(1, snuser, {"user": snuser.id, "category": staff2, "url": "https://www.kali.org/docs/", "weight": staff2.weight + snuser.id + 4, "description": "22"})
    insert(1, snuser, {"user": snuser.id, "category": staff1, "url": "https://getbootstrap.com/", "weight": staff1.weight + snuser.id + 5, "description": "23"})
    

    print('')
    print(models.SiteNav.fields_to_use())
    for obj in models.SiteNav.objects.all():
        print(list(obj.fields2dict().values()))


if __name__ == "__main__":
    main()

