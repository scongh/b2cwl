from django.conf.urls import url
from .views import IndexViews,LoginViews,CartViews

urlpatterns = [
    # 首页
    url(r'^$',IndexViews.myhome_index,name="myhome_index"),
    # 列表页
    url(r'^list/(?P<cid>[0-9]+)', IndexViews.myhome_list, name="myhome_list"),
    # 详情页
    url(r'^info/$', IndexViews.myhome_info, name="myhome_info"),


    # 登录
    url(r'^login/$', LoginViews.myhome_login, name="myhome_login"),
    # 执行登录
    url(r'^dologin/$', LoginViews.myhome_dologin, name="myhome_dologin"),
    # 退出登录
    url(r'^loginout/$', LoginViews.myhome_loginout, name="myhome_loginout"),

    # 注册
    url(r'^register/$', LoginViews.myhome_register, name="myhome_register"),
    # 执行注册
    url(r'^doregister/$', LoginViews.myhome_doregister, name="myhome_doregister"),
    # 短信发送
    url(r'^sendmsg/$', LoginViews.myhome_sendmsg, name="myhome_sendmsg"),
    # 短信接口
    # url(r'^hywxmsg/$', LoginViews.hywx_msg, name="hywx_msg"),

    # 购物车 增 删 改 查
    url(r'^cart/index/$', CartViews.myhome_cart_index, name="myhome_cart_index"),
    url(r'^cart/add/$', CartViews.myhome_cart_add, name="myhome_cart_add"),
    url(r'^cart/del/$', CartViews.myhome_cart_del, name="myhome_cart_del"),
    url(r'^cart/edit/$', CartViews.myhome_cart_edit, name="myhome_cart_edit"),
    #清空购物车
    url(r'^cart/clear/$', CartViews.myhome_cart_clear, name="myhome_myhome_cart_clear"),

]
