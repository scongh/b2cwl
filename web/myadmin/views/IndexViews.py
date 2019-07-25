from django.shortcuts import render
from django.http import HttpResponse,JsonResponse
from django.contrib.auth.hashers import make_password, check_password

# 登录验证
from django.contrib.auth import authenticate,login,logout
# Create your views here.
# 首页
def index(request):
    return render(request,'myadmin/index.html')


# 登录界面
def myadmin_login(request):
	return render(request,'myadmin/login.html')

# 登录处理
def myadmin_dologin(request):
    # try:
    # # 验证码 验证
    #     if(request.session.get('verifycode').upper() != request.POST.get('vcode').upper()):
    #         return HttpResponse('<script>alert("验证码错误！");history.back(-1);</script>')

    #     # 管理员和密码 是否正确
    #     if(request.POST.get('username') != 'admin' or request.POST.get('password') != r'123456'): 
    #         return HttpResponse('<script>alert("管理员账号或密码错误！");history.back(-1);</script>')

    #     request.session['AdminUser'] = {'username':'admin','uid':10}
    #     return render(request,'myadmin/index.html')
    # except:
    #     return HttpResponse('<script>alert("请先登录");location.href="/myadmin/login/";</script>')

    # 验证码检测
    if(request.session.get('verifycode').upper() != request.POST.get('vcode').upper()):
        return HttpResponse('<script>alert("验证码错误！");history.back(-1);</script>')
    # 管理员+密码 检测
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request,username=username,password=password)
    if user is not None:
        login(request,user) # 登录状态
        request.session['AdminUser']={'username':user.username,'uid':user.id}
        return render(request,'myadmin/index.html')

    return HttpResponse('<script>alert("管理员账号或密码错误！");history.back(-1);</script>')

# 退出登录
def myadmin_uplogin(request):
    # 撤销登录状态
    request.session['AdminUser'] = {}
    logout(request) # 退出登录

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


# 权限管理 + 权限分配 --- 管理员、权限、权限组
from django.contrib.auth.models import User,Permission,Group
# 管理员管理
# 列表
def myadmin_authuser_index(request):
    data = User.objects.all()
    context = {'userdata':data}
    return render(request,'myadmin/auth/auth_index.html',context)
# 添加管理员    
def myadmin_authuser_add(request):
    grouplist = Group.objects.all()
    context = {'grouplist':grouplist}

    return render(request,'myadmin/auth/auth_add.html',context)
#　执行添加
def myadmin_authuser_insert(request):
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    # print(data)
    data.pop('prms')
     
    # {'password': '', 'is_superuser': '0', 'email': '1414984944@qq.com', 'username': 'cong'}
    # 判断是否为超级用户 -- 密码自动加密
    if data['is_superuser'] == '1':
        # 创建超级用户
        data['is_superuser'] = True
        ob = User.objects.create_superuser(**data)
    else:     
        ob = User.objects.create_user(**data)

    # 判断是否分配组
    gs = request.POST.getlist('prms')
    # print(gs)
    if gs:
        # 给当前用户分配组
        ob.groups.set(gs)
        ob.save()

    return HttpResponse('<script>alert("管理员创建成功");location.href="/myadmin/auth/user/idnex/";</script>')
# 删除
def myadmin_authuser_del(request):
    # 接收id，获取对象
    aid = request.GET.get('aid')
    # print(aid)

    # 判断是否为 超级用户
    res =  User.objects.get(id=aid)
    # print(res.is_superuser)
    if res.is_superuser:
        return JsonResponse({'msg': '超级用户不可删除', 'code': 1})

    # 执行删除
    ob = User.objects.get(id=aid) # 会自动把 外键表也删了
    ob.delete()

    return JsonResponse({'msg': '删除成功', 'code': 0})
# 编辑
def myadmin_authuser_edit(request):
    # 接受管理员id
    uid = request.GET.get('uid')
    # 获取对象
    uob = User.objects.get(id=uid)
    # print(uob.id,uob,uob.email,uob.is_superuser,uob.password)
    # return HttpResponse('<script>alert("更新成功");</script>')

    # print(uid)
    # # 判读当前的请求方式
    if request.method == 'POST':
        # 执行更新操作
        if request.POST.get('password',None):
            uob.password = make_password(request.POST['password'], None, 'pbkdf2_sha256')

        # 更新其他数据
        uob.username = request.POST.get('username')
        uob.email = request.POST.get('email')

        # 判断是否有权限组
        prms = request.POST.getlist('prms', None)
        # 先删除(清空)权限组，再添加
        uob.groups.clear()
        if prms:
            # 再添加权限组
            uob.groups.set(prms)
        uob.save()
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/auth/user/idnex/";</script>')

    elif request.method == 'GET':
        # 获取权限组信息，排出已选定的权限
        grouplist = Group.objects.exclude(user=uob)
        # 自带的权限组
        # groupli = Group.objects.filter(user=uob)
        # 显示编辑表单
        context = {'uinfo': uob, 'grouplist': grouplist}
        return render(request, 'myadmin/auth/authedit.html/', context)


# 权限组管理
def myadmin_authgroup_index(request):
    data = Group.objects.all()
    context = {'groupdata':data}
    return render(request,'myadmin/auth/group_index.html',context)

def myadmin_authgroup_add(request):
    # 读取权限数据、排去以Can开头的－－系统默认生成的权限
    perms = Permission.objects.exclude(name__istartswith='Can')
    # for i in perms:
    #     print(i)
    context = {'perms':perms}
    return render(request,'myadmin/auth/group_add.html',context)

def myadmin_authgroup_insert(request):
    # data = request.POST.dict()
    # data.pop('csrfmiddlewaretoken')
    # print(data)

    # 组名
    name = request.POST.get('group_name')
    # 权限
    prms = request.POST.getlist('prms')
    # print(name)
    # print(prms)

    # 创建组
    g = Group(name=name)
    g.save()
    # 权限分配-- 有权限则添加
    if prms:
        # 外键
        g.permissions.set(prms)
        g.save()
    return HttpResponse('<script>alert("权限组创建成功");location.href="/myadmin/auth/group/idnex/";</script>')

def myadmin_authgroup_del(request):
    # 接收id，获取对象
    aid = request.GET.get('aid')
    # print(aid)

    # 判断管理组 是否有 管理员 i.user_set.count = 0
    res = Group.objects.get(id=aid)
    # print(1111111,res.user_set.count())
    if res.user_set.count()>0:
        return JsonResponse({'msg': '该组存在管理员，不可删除', 'code': 1})

    # 执行删除
    ob = Group.objects.get(id=aid)  # 会自动把 外键表也删了
    ob.delete()

    return JsonResponse({'msg': '删除成功', 'code': 0})

def myadmin_authgroup_edit(request):
    # 接受管理员id
    gid = request.GET.get('gid')
    # 获取对象-权限组
    gob = Group.objects.get(id=gid)
    # pob = gob.permissions.name
    # sob = Permission.objects.getlist()

    # 判读当前的请求方式
    if request.method == 'POST':
        # 更新其他数据
        gob.name = request.POST.get('name')
        # 判断是否有权限
        prms = request.POST.getlist('prms',None)
        # 先删除(清空)权限，再添加
        gob.permissions.clear()
        if prms:
            # 再添加权限
            gob.permissions.set(prms)
        gob.save()
        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/auth/group/idnex/";</script>')

    elif request.method == 'GET':
        # 获取权限信息，后排出已选定的权限，在排除系统权限
        perms = Permission.objects.exclude(group=gob).exclude(name__istartswith='can')
        # 显示编辑表单
        context = {'ginfo': gob, 'grouplist':perms}
        return render(request,'myadmin/auth/groupedit.html/', context)