from django.shortcuts import render
from django.http import HttpResponse,JsonResponse

def myhome_pay_result(request):
    pass



# from web import settings
# from utils.pay import AliPay
# # AliPay 对象实例化
# def Get_AliPay_Object():
#     alipay = AliPay(
#         appid=settings.ALIPAY_APPID,  # APPID （沙箱应用）
#         app_notify_url=settings.ALIPAY_NOTIFY_URL,  # 回调通知地址
#         return_url=settings.ALIPAY_RETURN_URL,  # 支付完成后的跳转地址
#         app_private_key_path=settings.APP_PRIVATE_KEY_PATH,  # 应用私钥
#         alipay_public_key_path=settings.ALIPAY_PUBLIC_KEY_PATH,  # 支付宝公钥
#         debug=True,  # 默认False, -- 沙箱环境
#     )
#     return alipay