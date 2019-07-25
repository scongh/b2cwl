from django.db import models

# Create your models here.


# 定义会员模型
class Users(models.Model):
    nikename = models.CharField(max_length=20,null=True)
    password = models.CharField(max_length=77)
    # phone = models.CharField(max_length=11,unique=True)
    phone = models.CharField(max_length=11)
    email = models.CharField(max_length=100)
    age = models.IntegerField(null=True)
    pic_url = models.CharField(max_length=100)
    SEX_CHOICES = (
        (0, '女'),
        (1, '男'),
    )
    sex = models.CharField(max_length=1,null=True,choices=SEX_CHOICES)
    # 0 正常  1禁用  2 删除 ....
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)

    # 自定义会员管理权限
    class Meta:
        permissions = (
            ('show_Users','查看会员列表权限'),
            ('create_Users','添加会员权限'),
            ('edit_Users','修改会员信息权限'),
            ('remove_Users','删除会员权限'),
        )


# 商品分类  -- 无限分类(一般2~3级)
class Cates(models.Model):
    name = models.CharField(max_length=32)
    pid = models.IntegerField() # 父类id
    path = models.CharField(max_length=50)
    # 自定义商品分类管理权限
    class Meta:
        permissions = (
            ('show_Cates','查看商品分类列表权限'),
            ('create_Cates','添加商品分类权限'),
            ('edit_Cates','修改商品分类信息权限'),
            ('remove_Cates','删除商品分类权限'),
        )

# 商品模型
class Goods(models.Model):
    # 所属分类id 、商品name、商品标题、价格、数量、图片-路径、商品的描述、销量、点击次数
    cateid = models.ForeignKey(to='Cates', to_field='id') # 多对一
    goodsname = models.CharField(max_length=50)
    title = models.CharField(max_length=255)
    price = models.FloatField()
    goodsnum = models.IntegerField()
    pic_url = models.CharField(max_length=255)
    goodsinfo = models.TextField()
    ordernum = models.IntegerField(default=0)
    clicknum = models.IntegerField(default=0)
    # 状态--0新品、1热卖、2推荐、3下架   、 添加时间
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True)
    # 自定义会员管理权限
    class Meta:
        permissions = (
            ('show_Goods','查看商品列表权限'),
            ('create_Goods','添加商品权限'),
            ('edit_Goods','修改商品信息权限'),
            ('remove_Goods','删除商品权限'),
        )



# 购物车模型
class Cart(models.Model):
    # id 用户id 商品id 数量
    uid = models.ForeignKey(to="Users", to_field="id") # 多对一 绑定会员id
    goodsid = models.ForeignKey(to="Goods", to_field="id")
    num = models.IntegerField()


# 订单模型
class Order(models.Model):
    # 多对一 绑定会员id
    uid = models.ForeignKey(to="Users", to_field="id")
    username = models.CharField(max_length=20) #会员名
    phone = models.CharField(max_length=15)
    address = models.CharField(max_length=255) #地址
    totalprice = models.FloatField() #总价
    # 0未支付、1已支付、2已发货、3已收货、4已评论
    status = models.IntegerField(default=0)
    addtime = models.DateTimeField(auto_now_add=True) # 添加时间
    paytime = models.DateTimeField(null=True) # 付款时间

    paytype = models.IntegerField(default=0) # 支付类型
    # 自定义会员管理权限
    class Meta:
        permissions = (
            ('show_Order','查看订单列表权限'),
            # 订单没有添加
            ('create_Order','添加订单权限'),
            ('edit_Order','修改订单信息权限'),
            ('remove_Order','删除订单权限'),
        )


#　订单详情
class OrderInfo(models.Model):
    # 多对一 绑定订单id
    orderid = models.ForeignKey(to="Order", to_field="id")
    # 多对一 绑定商品id
    goodsid = models.ForeignKey(to='Goods', to_field="id")
    num = models.IntegerField()