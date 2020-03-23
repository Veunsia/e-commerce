from django.shortcuts import render


# Create your views here.
from UsrApp.models import AxfUser


def mine(request):
    user_id = request.session.get('user_id')
    if user_id:
        user = AxfUser.objects.get(pk=user_id)
        context = {
            'user_id':user_id,
            'user':user,
        }
        return render(request, 'axf/main/mine/mine.html',context=context)
    else:
        context={
            'msg': '未登录'
        }
        return render(request, 'axf/main/mine/mine.html',context=context)
