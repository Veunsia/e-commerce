from alipay import AliPay
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from AXF.settings import PRIVATE_KEY, PUBLIC_KEY
from CartApp.models import AxfCart
from CartApp.views import all_money
from OrederApp.models import AxfOrderGoods, AxfOrder


def can_create(request):
    user_id = request.session.get('user_id')
    carts = AxfCart.objects.filter(c_user_id=user_id)
    selected_carts = carts.filter(c_is_select=True)
    have_selected = selected_carts.exists()

    data = {}

    if have_selected:
        # 创建一个order对象
        order = AxfOrder()
        order.o_user_id = user_id
        order.o_price = all_money(user_id)
        order.save()

        for cart in selected_carts:
            aog = AxfOrderGoods()
            aog.aog_order = order
            aog.aog_goods = cart.c_goods
            aog.aog_num = cart.c_goods_num
            aog.save()
            cart.delete()

        data['msg'] = '存在已选择，可以下单'
        data['status'] = 200
        data['order_id'] = order.id
    else:
        data['msg'] = '不可以下单'
        data['status'] = 201

    return JsonResponse(data=data)


def orderDetail(request):
    order_id = request.GET.get('order_id')

    print(order_id)
    order = AxfOrder.objects.get(pk=order_id)

    context = {
        'order': order,
    }

    return render(request, 'axf/order/order_detail.html', context=context)


def testpay(request):
    alipay = AliPay(
        appid="2016101500690455",
        app_notify_url=None,  # 默认回调url
        app_private_key_string=PRIVATE_KEY,
        # 支付宝的公钥，验证支付宝回传消息使用，不是你自己的公钥,
        alipay_public_key_string=PUBLIC_KEY,
        sign_type="RSA2",  # RSA 或者 RSA2
        debug=False,  # 默认False
    )

    subject = "订单" + request.GET.get('order_id')
    total_money = request.GET.get('total_money')
    # 电脑网站支付，需要跳转到https://openapi.alipay.com/gateway.do? + order_string
    order_string = alipay.api_alipay_trade_page_pay(
        out_trade_no="20161112",
        total_amount=total_money,
        subject=subject,
        return_url="http://www.1000phone.com",
        notify_url="http://www.1000phone.com"  # 可选, 不填则使用默认notify url
    )

    return redirect('https://openapi.alipaydev.com/gateway.do?' + order_string)
