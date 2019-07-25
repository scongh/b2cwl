from django.conf.urls import url
from . views import IndexViews,UsersViews,CatesViews,GoodsViews

from .views import OrderViews

urlpatterns = [
    # 支付流程
    # url(r'^auth/group/edit/$', OrderViews.myhome_pay_result, name="myhome_pay_result"),

	# 登录
    url(r'^login/$',IndexViews.myadmin_login,name="myadmin_login"),
    # 登录处理 - 首页
    url(r'^dologin/$',IndexViews.myadmin_dologin,name="myadmin_dologin"),
    # 验证码
    url(r'^varifycode/$',IndexViews.varifycode,name="myadmin_vcode"),
    # 退出登录
    url(r'^uplogin/$',IndexViews.myadmin_uplogin,name="myadmin_uplogin"),


    # 首页
    url(r'^index/$',IndexViews.index,name="index"),


    # 会员管理
    url(r'^user/add/$',UsersViews.user_add,name="myadmin_user_add"),
    url(r'^user/insert/$',UsersViews.user_insert,name="myadmin_user_insert"),
    url(r'^user/index/$',UsersViews.user_index,name="myadmin_user_index"),
    # 会员用户的编辑
    url(r'^user/edit/$',UsersViews.user_edit,name="myadmin_user_edit"),
    # url(r'^user/update/$',UsersViews.user_edit,name='myadmin_user_update'),
    # 会员状态修改
    url(r'^user/setstatus/$',UsersViews.user_set_status,name='myadmin_user_set_status'),


    # 商品分类管理
    # 商品分类数据 添加
    url(r'^cate/add/$',CatesViews.cate_add,name="myadmin_cate_add"),
    # 商品分类列表
    url(r'^cate/index/$',CatesViews.cate_index,name="myadmin_cate_index"),
    # 商品分类删除
    url(r'^cate/del/$',CatesViews.cate_del,name="myadmin_cate_del"),
    # ----编辑
    url(r'^cate/edit/$',CatesViews.cate_edit,name="myadmin_cate_edit"),


    # 商品管理
    url(r'^good/add/$',GoodsViews.good_add,name="myadmin_good_add"),
    url(r'^good/insert/$',GoodsViews.good_insert,name="myadmin_good_insert"),

    url(r'^good/index/$',GoodsViews.good_index,name="myadmin_good_index"),
    # 删除goods_del
    url(r'^good/del/$',GoodsViews.good_del,name="myadmin_good_del"),
    # 编辑 -- 状态
    url(r'^good/status/$',GoodsViews.good_status,name="myadmin_good_status"),
    # 商品编辑
    url(r'^good/edit/$',GoodsViews.good_edit,name="myadmin_good_edit"),


    # 权限管理
    # 管理员管理
    url(r'^auth/user/idnex/$',IndexViews.myadmin_authuser_index,name="myadmin_authuser_index"), # 列表
    url(r'^auth/user/add/$',IndexViews.myadmin_authuser_add,name="myadmin_authuser_add"), # 添加
    url(r'^auth/user/insert/$',IndexViews.myadmin_authuser_insert,name="myadmin_authuser_insert"), # 执行添加
    url(r'^auth/user/del/$', IndexViews.myadmin_authuser_del, name="myadmin_authuser_del"),  # 删除
    url(r'^auth/user/edit/$', IndexViews.myadmin_authuser_edit, name="myadmin_authuser_edit"),  # 编辑

    # 权限组管理
    url(r'^auth/group/idnex/$',IndexViews.myadmin_authgroup_index,name="myadmin_authgroup_index"),
    url(r'^auth/group/add/$',IndexViews.myadmin_authgroup_add,name="myadmin_authgroup_add"),
    url(r'^auth/group/insert/$',IndexViews.myadmin_authgroup_insert,name="myadmin_authgroup_insert"),
    url(r'^auth/group/del/$', IndexViews.myadmin_authgroup_del, name="myadmin_authgroup_del"),
    url(r'^auth/group/edit/$', IndexViews.myadmin_authgroup_edit, name="myadmin_authgroup_edit"),



]
