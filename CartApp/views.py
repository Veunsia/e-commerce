from django.http import JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from CartApp.models import AxfCart
from MarketApp.models import AxfGoods


def cart(request):
    user_id = request.session.get('user_id')
    carts = AxfCart.objects.filter(c_user_id=user_id).order_by('-id')
    # goods_dict = dict()
    # for cart in carts:
    #     goods = AxfGoods.objects.get(pk=cart.c_goods_id)
    #     goods_dict[goods]=cart.c_goods_num
    money = 0
    for cart in carts.filter(c_is_select=True):
        money = round(money + cart.c_goods.price * cart.c_goods_num, 2)

    context = {
        # 'goods_dict':goods_dict,
        'carts': carts,
        'money': money,
        'isall': carts.filter(c_is_select=False).exists()
    }
    # print(money)
    # print(carts.filter(c_is_select=False).exists())
    return render(request, 'axf/main/cart/cart.html', context=context)


def addToCart(request):
    user_id = request.session.get('user_id')
    data = {

    }
    if user_id:
        good_id = request.GET.get('good_id')
        carts = AxfCart.objects.filter(c_goods_id=good_id)
        if carts.exists():
            cart = carts.first()
            cart.c_goods_num = cart.c_goods_num + 1
            cart.c_is_select = True

        else:

            cart = AxfCart()
            cart.c_user_id = user_id
            cart.c_goods_id = good_id
        cart.save()

        data['status'] = 200
        data['msg'] = '添加成功'
        data['c_goods_num'] = cart.c_goods_num
    else:
        data['status'] = 201
        data['msg'] = '未登录'

    return JsonResponse(data=data)


def subfromcart(request):
    user_id = request.session.get('user_id')
    data = {

    }
    if user_id:
        good_id = request.GET.get('good_id')
        carts = AxfCart.objects.filter(c_goods_id=good_id)
        cart = carts.first()
        try:
            if cart.c_goods_num > 0:
                cart.c_goods_num = cart.c_goods_num - 1
                cart.save()
            else:
                cart.delete()

            data['status'] = 200
            data['msg'] = '删除成功'
            data['c_goods_num'] = cart.c_goods_num
        except AttributeError:
            pass

    else:
        data['status'] = 201
        data['msg'] = '未登录'

    return JsonResponse(data=data)


@csrf_exempt
def subgoods(request):
    user_id = request.session.get('user_id')

    cart_id = request.POST.get('cartid')
    cart = AxfCart.objects.get(pk=cart_id)
    data = {
        'msg': 'sub ok',
    }

    if cart.c_goods_num > 1:
        cart.c_goods_num = cart.c_goods_num - 1
        cart.save()
        data['c_goods_num'] = cart.c_goods_num
        data['status'] = 200
    else:
        cart.delete()
        data['status'] = 204
    isall = not AxfCart.objects.filter(c_user_id=user_id).filter(c_is_select=False).exists()
    data['money'] = all_money(user_id)
    data['isall'] = isall
    return JsonResponse(data=data)


def addgoods(request):
    user_id = request.session.get('user_id')

    cart_id = request.GET.get('cartid')

    cart = AxfCart.objects.get(pk=cart_id)
    cart.c_goods_num = cart.c_goods_num + 1
    cart.save()

    data = {
        'msg': 'ok',
        'status': 200,
        'c_goods_num': cart.c_goods_num,
        'money': all_money(user_id),
    }
    return JsonResponse(data=data)


def isselect(request):
    user_id = request.session.get('user_id')

    cart_id = request.GET.get('cartid')
    cart = AxfCart.objects.get(pk=cart_id)

    cart.c_is_select = not cart.c_is_select
    cart.save()

    isall = not AxfCart.objects.filter(c_user_id=user_id).filter(c_is_select=False).exists()

    data = {
        'msg': 'ok',
        'status': 200,
        'c_is_select': cart.c_is_select,
        'money': all_money(user_id),
        'isall': isall,
    }
    return JsonResponse(data=data)


def selectall(request):
    user_id = request.session.get('user_id')

    carts = AxfCart.objects.filter(c_user_id=user_id)

    data = {}

    if carts.filter(c_is_select=False).exists():
        for cart in carts.filter(c_is_select=False):
            cart.c_is_select = True
            cart.save()
            data['msg'] = '存在未选择的数据，全部选择'
            data['status'] = 200
            # data['money'] = all_money(user_id)
    else:
        for cart in carts:
            cart.c_is_select = False
            cart.save()
            data['msg'] = '不存在未选择的数据，全部取消选择'
            data['status'] = 201

    data['money'] = all_money(user_id)

    return JsonResponse(data=data)


def all_money(user_id):
    carts = AxfCart.objects.filter(c_user_id=user_id).filter(c_is_select=True)
    money = 0
    for cart in carts:
        money = round(money + cart.c_goods.price * cart.c_goods_num, 2)
    return money


