from django.shortcuts import render

# Create your views here.
from HomeApp.models import AxfWheel, AxfNav, AxfMustBuy, AxfMainShow


def home(request):
    wheels = AxfWheel.objects.all()

    navs = AxfNav.objects.all()

    must_buys = AxfMustBuy.objects.all()

    main_shows = AxfMainShow.objects.all()

    return render(request,'axf/main/home/home.html',context=locals())