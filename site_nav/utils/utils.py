import requests  
from bs4 import BeautifulSoup  


def get_title(url):  
    '''
    爬取url的http response的html的title

    Returns:
        string: title. 若失败，则为url
    '''
    if url is None or url == "":
        return url

    try:
        # 发送HTTP GET请求  
        response = requests.get(url, timeout=2)  
        # 检查请求是否成功  
        if response.status_code == 200:  
            # 解析HTML内容  
            soup = BeautifulSoup(response.text, 'html.parser')  
            # 获取<title>标签的内容  
            title = soup.title.string if soup.title else url
            return title  
        else:  
            return url 
    except Exception as e:
        return url


def set_default(dict_:dict, key, value):
    '''
    与python内置的setdefault的区别是：要检查key对应的value是否为None
    '''
    # !!! 注意：与python内置的setdefault的区别是：要检查key对应的value是否为None
    if key not in dict_ or dict_[key] is None:
        dict_[key] = value
    return dict_


def set_default_dd(dict_:dict, key, value:dict):
    '''
    为字典嵌套字典设置初始值
    '''
    set_default(dict_, key, value)
    for k, v in value.items():
        set_default(dict_[key], k, v)
    return dict_


def set_default_session(session, key, value):
    '''
    为request.session设置初始值
    '''
    if isinstance(value, dict):
        set_default_dd(session, key, value)
        # 注意一定要设置modified为True
        session.modified = True
    else:
        set_default(session, key, value)
    return session


def update_session(session, key, value:dict):
    '''
    为字典嵌套字典的session的一个key更新value
    '''
    session[key].update(value)
    # 注意一定要设置modified为True
    session.modified = True
    
