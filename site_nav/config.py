# whether to print debug info
IS_SITE_NAV_DEBUG = False
# Do NOT use this in any other source files!!!
# True: test this app purely alone; False: integrate with the "user" app
IS_SITE_NAV_TEST = True

ADMIN_ID = [1]


# define `User` for models.py and define `UserAPI`
if IS_SITE_NAV_TEST:
    from .tests.tests import User, UserAPI
else:
    from django.contrib.auth.models import User
    class UserAPI():
        def __init__(self, request):
            self.request = request
        
        @property
        def id(self):
            return self.request.user.id

        @property
        def username(self):
            return self.request.user.username
        
        @property
        def is_authenticated(self):
            return self.request.user.is_authenticated

        @staticmethod
        def login_url_name():
            return "login"

        @staticmethod
        def logout_url_name():
            return "logout"