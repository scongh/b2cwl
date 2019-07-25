from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
# 首页
def index(request):
    
    return render(request,'myadmin/index.html')


# 登录界面
def myadmin_login(request):
	return render(request,'myadmin/login.html')

# 登录处理
def myadmin_dologin(request):
    try:
    # 验证码 验证
        if(request.session.get('verifycode').upper() != request.POST.get('vcode').upper()):
            return HttpResponse('<script>alert("验证码错误！");history.back(-1);</script>')

        # 管理员和密码 是否正确
        if(request.POST.get('username') != 'admin' or request.POST.get('password') != r'123456'): 
            return HttpResponse('<script>alert("管理员账号或密码错误！");history.back(-1);</script>')

        request.session['AdminUser'] = {'username':'admin','uid':10}
        return render(request,'myadmin/index.html')
    except:
        return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/";</script>')

        
# 退出登录
def myadmin_uplogin(request):
    # 撤销登录状态
    request.session['AdminUser'] = {}
    # del request.session['AdminUser']
    # 返回登录界面
    return HttpResponse('<script>alert("退出成功！");location.href="/myadmin/login/";</script>')

# 验证码
# PIL -- 验证码
def varifycode(request):
    # 引入绘图模块
    from PIL import Image, ImageDraw, ImageFont
    # 引入随机函数模块
    import random
    # 定义变量，用于画面的背景色、宽、高
    bgcolor = (random.randrange(0, 250), random.randrange(100,200), 250)
    width = 100
    height = 25
    # 创建画面对象
    im = Image.new('RGB', (width, height), bgcolor)
    # 创建画笔对象
    draw = ImageDraw.Draw(im)
    # 调用画笔的point()函数绘制噪点 -- 干扰视觉
    for i in range(0, 100):
        xy = (random.randrange(0, width), random.randrange(0, height))
        fill = (random.randrange(0, 255), 250, random.randrange(0, 255))
        draw.point(xy, fill=fill)
    # 定义验证码的备选值
    str1 = 'ABCD123EFGHIJK456LMNOPQRS789TUVWXYZ0'
    # 随机选取4个值作为验证码
    rand_str = ''
    for i in range(0, 4):
        rand_str += str1[random.randrange(0, len(str1))]
    # 构造字体对象 -- 导入字体，找到字体的路径
    font = ImageFont.truetype('static/myadmin/assets/fonts/SketchFlow Print.ttf', 24) # 24为 字体大小
    # 构造字体颜色
    fontcolor = (255, random.randrange(0, 255), random.randrange(0, 255))
    # 绘制4个字 -- （5，2） x，y轴
    draw.text((5, 2), rand_str[0], font=font, fill=fontcolor)
    draw.text((25, 2), rand_str[1], font=font, fill=fontcolor)
    draw.text((50, 2), rand_str[2], font=font, fill=fontcolor)
    draw.text((75, 2), rand_str[3], font=font, fill=fontcolor)
    # 释放画笔
    del draw
    # 存入session，用于做进一步验证
    request.session['verifycode'] = rand_str
    # 内存文件操作
    import io
    buf = io.BytesIO()
    # 将图片保存在内存中，文件类型为png
    im.save(buf, 'png')
    # 将内存中的图片数据返回给客户端，MIME类型为图片png
    return HttpResponse(buf.getvalue(), 'image/png')


# 权限管理
def myadmin_authuser_index(request):
    return render(request,'myadmin/suth/index.html')
    
def myadmin_authuser_add(request):
    pass

def myadmin_authuser_insert(request):
    pass

def myadmin_authgroup_index(request):
    pass

def myadmin_authgroup_add(request):
    pass

def myadmin_authgroup_insert(request):
    pass