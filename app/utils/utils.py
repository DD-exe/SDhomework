import requests  
from bs4 import BeautifulSoup  
from urllib.parse import urlparse
from django.urls import resolve, reverse


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
        response = requests.get(url, timeout=1)  
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


def get_prev_url(request):
    '''
    获得当前请求页面的之前的页面，若之前的页面不存在或就是当前页面，则返回默认页面
    '''
    previous = request.headers.get("Referer")
    if previous is None:
        previous = reverse("app-site-nav") 
    else:
        previous = urlparse(previous)[2]
        previous = reverse("app-site-nav") if previous == request.path_info else previous
    return previous
