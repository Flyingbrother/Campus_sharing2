from django.shortcuts import render, redirect
from .models import *
from df_user.models import UserInfo
from df_user import user_decorator
from df_cart.models import *
from django.db import transaction
from datetime import datetime
from decimal import Decimal

# Create your views here.

@user_decorator.login
def order(request):
    #查询用户对象
    user = UserInfo.objects.get(id=request.session['user_id'])
    #根据提交查询购物车信息
    get = request.GET
    cart_ids = get.getlist('cart_id')
    cart_ids1 = [int(item) for item in cart_ids]
    carts = CartInfo.objects.filter(id__in=cart_ids1)
    #构造传递到模板中的数据
    context = {
        'title': '提交订单',
        'page_name': 1,
        'carts': carts,
        'user': user,
        'cart_ids': ','.join(cart_ids)
    }
    print(cart_ids)
    return render(request, 'df_order/order.html', context)


@transaction.atomic()
@user_decorator.login
def order_handle(request):
    tran_id = transaction.savepoint()
    #接受购物车编号

    cart_ids = request.POST.get('cart_ids')
    # print(cart_ids)
    # print('输出cart_ids')

    try:
        #创建订单对象
        order = OrderInfo()
        now = datetime.now()
        uid = request.session['user_id']
        order.oid = '%s%d' % (now.strftime('%Y%m%d%H%M%S'), uid)
        order.user_id = uid

        order.odate = now
        # print('在total之前')
        order.ototal = Decimal(request.POST.get('total'))
        # print('在total之后')
        order.save()

        #创建详单对象
        # print('创建详单')
        cart_ids1 = [int(item) for item in cart_ids.split(',')]#[45, 46]
        # print(cart_ids1)

        for id1 in cart_ids1:
            detail = OrderDetailInfo()
            detail.order = order
            #查询购物车信息
            # print('查询购物车信息')
            cart = CartInfo.objects.get(id=id1)
            #盘攒商品库存
            # print('盘赞商品库存')
            goods = cart.goods
            if goods.gkucun >= cart.count:#如果库存大于购买数量
                #判断商品库存
                # print('判断商品库存')
                goods.gkucun = cart.goods.gkucun - cart.count
                goods.save()
                #完善订单信息
                # print('完善订单信息')
                detail.goods_id = goods.id
                detail.price = goods.gprice
                detail.count = cart.count
                detail.save()
                # print('保存订单信息')
                #删除购物车数据
                cart.delete()
                # print('删除订单信息')
            else:#如果库存小于购买数量
                transaction.savepoint_rollback(tran_id)
                return redirect('/cart/')
                #return HttpResponse('no')
        transaction.savepoint_commit(tran_id)
    except Exception as e:
        print('===================%s' % e)
        transaction.savepoint_rollback(tran_id)

    # return HttpResponse('ok')
    # print('ok')
    return redirect('/user/order/')


@user_decorator.login
def pay(request, oid):
    order = OrderInfo.objects.get(oid=oid)
    order.oIsPay = True
    order.save()
    context = {
        'order': order
    }
    return render(request, 'df_order/pay.html', context)