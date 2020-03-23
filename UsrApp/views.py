import re
import uuid
from io import BytesIO

from PIL import Image, ImageFont
from PIL.ImageDraw import ImageDraw
from django.contrib.auth.hashers import make_password, check_password
from django.core.cache import cache
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse

from AXF import settings
from UsrApp.models import AxfUser
from UsrApp.viewsconstaint import send_email


def register(request):
    if request.method == 'GET':
        return render(request, 'axf/user/register/register.html')
    elif request.method == 'POST':
        user = AxfUser()
        name = request.POST.get('name')
        password = make_password(request.POST.get('password'))

        email = request.POST.get('email')
        icon = request.FILES.get('icon')
        print(icon)
        user.u_name = name
        user.u_password = password
        user.u_email = email
        user.u_icon = icon

        token = uuid.uuid4()
        user.u_token = token
        user.save()

        send_email(name, email, token)

        cache.set(token, user.id, timeout=45)

        return redirect(reverse('axfuser:login'))


def checkname(request):
    name = request.GET.get('name')
    user = AxfUser.objects.filter(u_name=name)
    if user:
        return JsonResponse(
            {
                'msg': '用户名已存在',
                'status': 201
            })
    else:
        return JsonResponse({
            'msg': '用户名可以使用',
            'status': 200
        })


def checkemail(request):
    token = request.GET.get('token')
    user_id = cache.get(token)
    if user_id:
        user = AxfUser.objects.get(pk=user_id)
        user.u_status = True
        user.save()
        cache.delete(token)
        return HttpResponse('激活成功')
    else:

        return HttpResponse('链接失效请重新激活')


def login(request):
    if request.method == 'GET':
        return render(request, 'axf/user/login/login.html')

    elif request.method == 'POST':
        # 获取用户输入的验证码
        y_code = request.POST.get('y_code')
        # 获取图片上的验证码
        verify_code = request.session.get('verify_code')

        if re.match(verify_code,y_code,re.IGNORECASE):

            name = request.POST.get('name')
            user = AxfUser.objects.filter(u_name=name)[0]
            password = request.POST.get('password')
            user_password = user.u_password

            if check_password(password, user_password) and user.u_status == True:
                request.session['user_id'] = user.id
                return redirect(reverse('axfmine:mine'))
            else:
                return render(request, 'axf/user/login/login.html')

        else:
            context = {
                'msg': '验证码错误'
            }
            return render(request, 'axf/user/login/login.html', context=context)


def checklogin(request):
    name = request.GET.get('name')
    user = AxfUser.objects.filter(u_name=name)
    if user:
        return JsonResponse(
            {
                'msg': '',
                'status': 200
            })
    else:
        return JsonResponse({
            'msg': '用户名不存在',
            'status': 201
        })


def get_code(request):
    # 初始化画布，初始化画笔

    mode = "RGB"

    size = (90, 45)

    red = get_color()

    green = get_color()

    blue = get_color()

    color_bg = (red, green, blue)

    image = Image.new(mode=mode, size=size, color=color_bg)

    imagedraw = ImageDraw(image, mode=mode)

    imagefont = ImageFont.truetype(settings.FONT_PATH, 40)

    verify_code = generate_code()

    request.session['verify_code'] = verify_code

    for i in range(4):
        fill = (get_color(), get_color(), get_color())
        imagedraw.text(xy=(20 * i, 0), text=verify_code[i], font=imagefont, fill=fill)

    for i in range(100):
        fill = (get_color(), get_color(), get_color())
        xy = (random.randrange(100), random.randrange(45))
        imagedraw.point(xy=xy, fill=fill)

    fp = BytesIO()

    image.save(fp, "png")

    return HttpResponse(fp.getvalue(), content_type="image/png")


import random


def get_color():
    return random.randrange(256)


def generate_code():
    source = "qwertyuiopasdfghjklzxcvbnm1234567890QWERTYUIOPASDFGHJKLZXCVBNM"

    code = ""

    for i in range(4):
        code += random.choice(source)

    return code


def logout(request):
    request.session.flush()
    return redirect(reverse('axfmine:mine'))