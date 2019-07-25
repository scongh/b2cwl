from django.shortcuts import render
from django.http import HttpResponse
import re

class AdminLoginMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        '''
        # 检测当前的请求是否已经登录,如果已经登录,.则放行,如果未登录,则跳转到登录页
        # 获取当前用户的请求路径  /admin/开头  但不是 /admin/login/  /admin/dologin/   /admin/verifycode
        urllist = ['/admin/login','/admin/dologin','/admin/vcode']
        # 判断是否进入了后台,并且不是进入登录页面
        if re.match('/admin/',request.path) and request.path not in urllist:

            # 检测session中是否存在 adminlogin的数据记录
            if request.session.get('Vuser','') == '':
                # 如果在session没有记录,则证明没有登录,跳转到登录页面
                return HttpResponse('<script>alert("请先登录");location.href="/admin/login";</script>')
        '''

        # 用户的请求路径
        path =request.path
        # 开通的访问的路由--登录、登录处理、验证码
        arr = ['/myadmin/login/','/myadmin/dologin/','/myadmin/varifycode/']
        # 检测会员是否访问 后台 -- re开头检测
        if(re.match('/myadmin/',path) and path not in arr):
            AdminUser = request.session.get('AdminUser',None)
            # 是否已经登录
            if not AdminUser:
               
                return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/";</script>')

        # 放行--该有的相应内容都响应
        response = self.get_response(request)
        return response