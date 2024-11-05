import re
from django.core.exceptions import ValidationError


def validate_username(value):
    # 正则表达式：允许字母、数字、汉字和下划线
    if not re.match(r'^[\w\u4e00-\u9fa5]+$', value):
        raise ValidationError(
            '用户名只能包含字母、数字、汉字和下划线中的几种。'
        )

def validate_password(value):
    if not re.match(r'^[a-zA-Z0-9_]+$', value):
        raise ValidationError(
            '密码只能包含字母、数字和下划线中的几种。'
        )
    # 检查字符类型
    has_letter = bool(re.search(r'[a-zA-Z]', value))
    has_digit = bool(re.search(r'\d', value))
    has_underscore = '_' in value

    # 计算满足的字符类型数量
    types_count = sum([has_letter, has_digit, has_underscore])

    # 验证至少有两种类型
    if types_count < 2:
        raise ValidationError(
            '密码必须包含至少两种字符类型：字母、数字和下划线。'
        )

def validate_name(value):
    # 正则表达式：只允许字母和中文字符
    if not re.match(r'^[a-zA-Z\u4e00-\u9fa5]+$', value):
        raise ValidationError('名字只能包含英文字母和中文字符')