from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

from . CatesViews import get_cates_all # 商品分类下拉框函数
from . UsersViews import uploads_pic # 图片处理函数
from .. models import Cates,Goods

from django.db.models import Q

from django.contrib.auth.decorators import permission_required

# Create your views here.
# show
# create
# edit
# remove
# 商品添加 -- 内容填写页面
@permission_required('myadmin.create_Goods',raise_exception=True)
def good_add(request):
    # 下拉框
    data = Cates.objects.all()
    catelist = get_cates_all(data)
    # 分配
    context = {'catelist': catelist} # catelist 为里面的数据  


    return render(request,'myadmin/goods/add.html',context)

# 商品添加-执行
# @permission_required('myadmin.create_Goods',raise_exception=True)
def good_insert(request):
	# 接收表单数据
    data = request.POST.dict()
    data.pop('csrfmiddlewaretoken')
    # print(111,data)
    # return HttpResponse('添加成功')
    data['cateid'] = Cates.objects.get(id = data['cateid'])

    # 头像上传
    # 接收上传的文件
    myfile = request.FILES.get('pic',None)
    if not myfile:
        # 没有选择头像上传,
        return HttpResponse('<script>alert("没有商品图片上次上传");history.back(-1);</script>')

    # 处理头像的上传  1.jpg ==> [1,jpg]
    data['pic_url'] = uploads_pic(myfile)

    # print(data)
    
    try:
        # 创建模型,添加数据
        ob = Goods(**data)
        ob.save()
        return HttpResponse('<script>alert("添加成功");location.href="/myadmin/good/index/";</script>')
    except:
        pass
    return HttpResponse('<script>alert("添加失败");history.back(-1);</script>')

# 商品列表
@permission_required('myadmin.show_Goods',raise_exception=True)
def good_index(request):
    
    # data = Cates.objects.all()
    # data = get_cates_all(data)
    data = Goods.objects.all()

    # 获取搜索条件
    types = request.GET.get('types',None)
    keywords = request.GET.get('keywords',None)
    # 搜索判断
    if types=="all":#price cateid
        # # 父类查询
        # res = Cates.objects.filter(name__contains = keywords)
        # for i in res:
        #     data = data.filter(cateid=i.id)
            
        data = data.filter(Q(id__contains = keywords) | Q(goodsname__contains = keywords))

    # 价格区间
    # elif types=="price":
    #     data = data.filter(id__contains = keywords)
    # 所属分类
    elif types=="cateid":
        # 父类查询
        res = Cates.objects.filter(name__contains = keywords)
        for i in res:
            data = data.filter(cateid=i.id)

        # [data.filter(cateid=i.id) for i in res]
        # data = data.filter(cateid__in=[data.filter(cateid=i.id).pid for i in res])
    elif types:
        search = {types+'__contains': keywords}
        data = data.filter(**search)

    # 导入分页类
    from django.core.paginator import Paginator
    p = Paginator(data, 10) # 实例化
    # 获取当前的页码数
    page_index = request.GET.get('page',1)
    # 获取当前 页数
    user_list = p.page(page_index)

    context = {'goodslist': data,'userlist': user_list}

    return render(request,'myadmin/goods/index.html',context)

@permission_required('myadmin.remove_Goods',raise_exception=True)
# 商品分类删除
def good_del(request):

    # this window--窗体对象 --> 文档对象(DOM), location(地址对象), history(历史对象)

    # 接收id，获取对象
    gid = request.GET.get('gid')

    # 判断是否为下架状态
    res = Goods.objects.filter(id=gid).filter(status='3').exists()#.count()
    print(gid,res)

    if not res:
        return JsonResponse({'msg':'该商品正在销售，不可删除','code':1})

    # 执行删除
    ob = Goods.objects.get(id=gid)
    ob.delete()

    return JsonResponse({'msg':'删除成功','code':0})

# 商品状态修改
@permission_required('myadmin.edit_Goods',raise_exception=True)
def good_status(request):
    # 通过uid获取 会员对象
    ob = Goods.objects.get(id=request.GET.get('gid'))
    # print(request.GET.get('gid'))
    # print(request.GET.get('status'))
    ob.status = request.GET.get('status')
    ob.save()
    return JsonResponse({'msg':'状态更新成功','code':0})

# 商品信息修改
@permission_required('myadmin.edit_Goods',raise_exception=True)
def good_edit(request):
    # 接受会员用户id
    gid = request.GET.get('gid')
    # 获取会员用户对象
    gob = Goods.objects.get(id=gid)

    # 判读当前的请求方式
    if request.method == 'POST':
        # 执行更新操作

        # 判断头像是否更新
        myfile = request.FILES.get('pic',None)
        if myfile:
            # 有新头像上传，则先删除原头像
            os.remove(BASE_DIR+gob.pic_url)
            # 更新头像
            uob.pic_url = uploads_pic(myfile)

        # 更新其他数据 --- 存对象Cates.objects.get(id=request.POST.get('cateid'))
        gob.cateid = Cates.objects.get(id=request.POST.get('cateid'))
        gob.goodsname = request.POST.get('goodsname')
        gob.title = request.POST.get('title')
        gob.price = request.POST.get('price')
        gob.goodsnum = request.POST.get('goodsnum')
        gob.goodsinfo = request.POST.get('goodsinfo')
        # print(gob.cateid,request.POST.get('cateid'))
        gob.save()

        return HttpResponse('<script>alert("更新成功");location.href="/myadmin/good/index/";</script>')

    elif request.method == 'GET':
        
        # 下拉框
        data = Cates.objects.all()
        catelist = get_cates_all(data)
        # 分配
        # catelist 为里面的数据  
        context = {'ginfo': gob,'catelist': catelist}
        return render(request,'myadmin/goods/edit.html/',context)
