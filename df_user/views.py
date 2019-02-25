from django.shortcuts import render, redirect
from .models import *
from hashlib import sha1
from django.http import JsonResponse, HttpResponseRedirect
from . import user_decorator
from df_goods.models import GoodsInfo
from df_order.models import *
from django.core.paginator import Paginator, Page
from hashlib import sha1
from .redisHelper import redisHelper
from django.http import HttpResponse



'''验证码'''
def verifyCode(request):
    from PIL import Image, ImageDraw, ImageFont
    import random
    # 创建背景颜色
    bgColor = (random.randrange(50, 100), random.randrange(50, 100), 0)
    # 规定宽高
    # width = 100
    # height = 25
    width = 120
    height = 30
    # 创建画布
    image = Image.new('RGB', (width, height), bgColor)
    # 构造字体对象
    font = ImageFont.truetype('arial.ttf', 22)
    # 创建画笔
    draw = ImageDraw.Draw(image)
    # 创建文本内容
    text = '0123456789ABCDEFGHIGKLMNOPQRSTUVWSYZ'
    # 逐个绘制字符
    textTemp = ''
    for i in range(4):
        textTemp1 = text[random.randrange(0, len(text))]
        textTemp += textTemp1
        draw.text(
            (i*30, 0),
            textTemp1,
            (255, 255, 255),
            font
        )

    request.session['code'] = textTemp
    # 保存到内存流中
    import io
    buf = io.BytesIO()
    image.save(buf, 'png')
    # 将内存流中的内容输出到客户端
    return HttpResponse(buf.getvalue(), 'image/png')


def register(request):
    return render(request, 'df_user/register.html')



def register_handle(request):
    #接受用户输入
    post = request.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    upwd2 = post.get('cpwd')
    uemail = post.get('email')
    code1 = post.get('code1')
    code2 = request.session['code']

    #判断验证码是否正确
    if code1 != code2:

        return redirect('/user/register')

    #判断俩次密码
    if upwd != upwd2:
        return redirect('/user/register')

    #判断用户名是否存在
    count = UserInfo.objects.filter(uname=uname).count()
    if count == 1:
        return redirect('/user/register')


    #密码加密
    s1 = sha1()
    s1.update(upwd.encode("utf8"))
    upwd3 = s1.hexdigest()

    #创建对象
    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()
    #注册成功，转到登录页面
    return redirect('/user/login/')


def register_exist(request):
    uname = request.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()

    return JsonResponse({'count': count})


def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)


def login_handle(request):
    #接受请求数据
    post = request.POST
    uname = post.get('username')
    upwd = post.get('pwd')
    jizhu = post.get('jizhu', 0)
    #根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)#[]
    # print(uname)
    #判断：如果未查到则用户名错误，如果查到则判断密码是否正确，正确则转到用户中心
    # if len(users) == 1:
    #     s1 = sha1()
    #     s1.update(upwd.encode("utf8"))
    #     if s1.hexdigest() == users[0].upwd:
    #         red = HttpResponseRedirect('/user/info/')
    #         #记住用户名
    #         if jizhu != 0:
    #             red.set_cookie('uname', uname)
    #         else:
    #             red.set_cookie('uname', '', max_age=-1)
    #         request.session['user_id'] = users[0].id
    #         request.session['user_name'] = uname
    #         return red
    #     else:
    #         context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
    #         return render(request, 'df_user/login.html', context)
    # else:
    #     context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
    #     return render(request, 'df_user/login.html', context)



    r = redisHelper('192.168.147.122', 6379)

    if r.get(uname)==None:


        if len(users) == 1:
            s1 = sha1()
            s1.update(upwd.encode("utf8"))
            if s1.hexdigest() == users[0].upwd:
                red = HttpResponseRedirect('/user/info/')
                #记住用户名
                if jizhu != 0:
                    red.set_cookie('uname', uname)
                else:
                    red.set_cookie('uname', '', max_age=-1)
                request.session['user_id'] = users[0].id
                request.session['user_name'] = uname
                r.set(uname, users[0].upwd)
                return red
            else:
                context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
                return render(request, 'df_user/login.html', context)
        else:
            context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)


    else:
        s1 = sha1()
        s1.update(upwd.encode("utf8"))
        if r.get(uname).decode() == s1.hexdigest():
            red = HttpResponseRedirect('/user/info/')
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            r.set(uname, users[0].upwd)
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname, 'upwd': upwd}
            return render(request, 'df_user/login.html', context)



def logout(request):
    request.session.flush()
    return redirect('/user/login/')


@user_decorator.login
def info(request):
    user_email = UserInfo.objects.get(id=request.session['user_id']).uemail
    user_address = UserInfo.objects.get(id=request.session['user_id']).uaddress
    #最近浏览
    goods_ids = request.COOKIES.get('goods_ids', '')
    goods_ids1 = goods_ids.split(',')

    # GoodsInfo.objects.filter(id__in=goods_ids1) #可以查出来商品信息，但不能维护顺序

    good_list = []
    for goods_id in goods_ids1:
        if goods_id != '':
            good_list.append(GoodsInfo.objects.get(id=int(goods_id)))
    context = {
        'title': '用户中心',
        'user_email': user_email,
        'user_address': user_address,
        'user_name': request.session['user_name'],
        'page_name': 1,
        'goods_list': good_list
    }
    return render(request, 'df_user/user_center_info.html', context)


@user_decorator.login
def order(request):
    order = OrderInfo.objects.filter(user_id=request.session['user_id'])
    # order1 = OrderDetailInfo.objects.filter(order_id=order.oid)

    orderdetail = OrderDetailInfo.objects.all()

    # paginator = Paginator(order, 1)
    # page = paginator.page(int(pindex))
    context = {'title': '用户中心',
               'page_name': 1,
               'order': order,
               'orderdetail': orderdetail,
               # 'Page': page,
               # 'paginator': paginator
               }
    return render(request, 'df_user/user_center_order.html', context)


@user_decorator.login
def site(request):
    user = UserInfo.objects.get(id=request.session['user_id'])
    if request.method == 'POST':
        post = request.POST
        user.ushou = post.get('ushou')
        user.uaddress = post.get('uaddress')
        user.uyoubian = post.get('uyoubian')
        user.uphone = post.get('uphone')
        user.save()
    context = {'title': '用户中心', 'user': user, 'page_name': 1}
    return render(request, 'df_user/user_center_site.html', context)








