import re

from django.shortcuts import render

# Create your views here.
from MarketApp.models import AxfFoodType, AxfGoods
from MarketApp.view_help import SORT_RULE_NUM_DOWN, SORT_RULE_SYN, SORT_RULE_PRICE_UP, SORT_RULE_PRICE_DOWN, \
    SORT_RULE_NUM_UP


def market(request):
    # 获取页面传过来的typeid、childcid、sort_rule
    foodtypeid = request.GET.get('foodtypeid', '104749')
    childcid = request.GET.get('childcid', '0')
    cur_sort_rule = request.GET.get('cur_sort_rule', '1')

    # 侧边栏
    foodtypes = AxfFoodType.objects.all()

    all_type = AxfFoodType.objects.filter(typeid=foodtypeid)[0]
    # 分类列表

    '''
    child_types_list = re.findall(r'[\u4e00-\u9fa5]+',all_type.childtypenames)
    # print(types_list)
    # 分类对应的id
    child_type_num_list = re.findall(r'[\d]+',all_type.childtypenames)
    # print(type_num_list)

    # 分类的字典
    type_dict = dict(zip(child_types_list,child_type_num_list))
    print(type_dict)
    
    '''
    childname_list = []
    childtypenames = all_type.childtypenames
    childtypenames_list = childtypenames.split('#')
    for childtype in childtypenames_list:
        childtypename = childtype.split(':')
        childname_list.append(childtypename)

    goods = AxfGoods.objects.filter(categoryid=int(foodtypeid))
    # 当前条目对应的商品
    if childcid == '0':
        pass
    else:
        goods = goods.filter(childcid=int(childcid))

    sort_rule_list = [
        ['综合排序', SORT_RULE_SYN],
        ['价格升序', SORT_RULE_PRICE_UP],
        ['价格降序', SORT_RULE_PRICE_DOWN],
        ['销量升序', SORT_RULE_NUM_UP],
        ['销量降序', SORT_RULE_NUM_DOWN],
    ]

    if cur_sort_rule == SORT_RULE_SYN:
        pass
    elif cur_sort_rule == SORT_RULE_PRICE_UP:
        goods = goods.order_by('price')
    elif cur_sort_rule == SORT_RULE_PRICE_DOWN:
        goods = goods.order_by('-price')
    elif cur_sort_rule == SORT_RULE_NUM_UP:
        goods = goods.order_by('productnum')
    elif cur_sort_rule == SORT_RULE_NUM_DOWN:
        goods = goods.order_by('-productnum')

    context = {
        'foodtypes': foodtypes,
        'foodtypeid': foodtypeid,
        'goods': goods,
        # 'types_list':types_list,
        # 'type_num_list':type_num_list,
        # 'type_dict': type_dict,
        'childname_list': childname_list,
        'childcid': childcid,
        'sort_rule_list': sort_rule_list,
        'cur_sort_rule': cur_sort_rule,
    }

    return render(request, 'axf/main/market/market.html', context=context)
