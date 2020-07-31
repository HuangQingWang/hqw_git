from django.shortcuts import render,redirect
import os,time,random
# Create your views here.


from .models import Wheel,Nav,Mustbuy,Mimianshop,FoodTypes,Goods,User,Cart,Order


def initdatabases(request):
    import xlrd, xlwt

    rootpath = os.getcwd()
    #开始存放轮播的的数据
    wheelexcelpath = os.path.join(rootpath, r'static\main\img\wheel\wheel.xlsx')
    workbook = xlrd.open_workbook(wheelexcelpath)
    xlxpath = workbook.sheet_names()
    content = workbook.sheet_by_name(xlxpath[0])
    nrows = content.nrows
    for i in range(1, nrows):
        cell_a = content.cell(i, 0).value
        imgpath = os.path.join(r"\static\main\img\wheel", cell_a)
        imgname = content.cell(i, 1).value
        trackid = content.cell(i, 2).value
        wheelimg = Wheel.objects.create(img=imgpath, name=imgname, trackid=trackid)
    xWheel = Wheel.objects.all()
    #开始存放nav的数据
    navexcelpath  = os.path.join(rootpath, r'static\main\img\nav\nav.xlsx')
    navworkbook = xlrd.open_workbook(navexcelpath)
    navxlxpath = navworkbook.sheet_names()
    navcontent = navworkbook.sheet_by_name(navxlxpath[0])
    nrows = navcontent.nrows
    for i in range(1, nrows):
        cell_a = navcontent.cell(i, 0).value
        imgpath = os.path.join(r"\static\main\img\nav", cell_a)
        imgname = navcontent.cell(i, 1).value
        trackid = navcontent.cell(i, 2).value
        navimg = Nav.objects.create(img=imgpath, name=imgname, trackid=trackid)
    #开始存放mustbuy的数据
    navexcelpath  = os.path.join(rootpath, r'static\main\img\mustbuy\mustbuy.xlsx')
    navworkbook = xlrd.open_workbook(navexcelpath)
    navxlxpath = navworkbook.sheet_names()
    navcontent = navworkbook.sheet_by_name(navxlxpath[0])
    nrows = navcontent.nrows
    for i in range(1, nrows):
        cell_a = navcontent.cell(i, 0).value
        imgpath = os.path.join(r"\static\main\img\mustbuy", cell_a)
        imgname = navcontent.cell(i, 1).value
        trackid = navcontent.cell(i, 2).value
        navimg = Mustbuy.objects.create(img=imgpath, name=imgname, trackid=trackid)
    #########
    navexcelpath  = os.path.join(rootpath, r'static\main\img\mimianshop\mimianshop.xlsx')
    navworkbook = xlrd.open_workbook(navexcelpath)
    navxlxpath = navworkbook.sheet_names()
    navcontent = navworkbook.sheet_by_name(navxlxpath[0])
    nrows = navcontent.nrows
    for i in range(1, nrows):
        cell_a = navcontent.cell(i, 0).value
        imgpath = os.path.join(r"\static\main\img\mimianshop", cell_a)
        imgname = navcontent.cell(i, 1).value
        trackid = navcontent.cell(i, 2).value
        navimg = Mimianshop.objects.create(img=imgpath, name=imgname, trackid=trackid)


    return render(request, 'axf/initdatabases.html', {"title": xWheel})

def home(request):
    wheelslist = Wheel.objects.all()
    navlist = Nav.objects.all()
    mustbuylist = Mustbuy.objects.all()
    mianmilist = Mimianshop.objects.all()[0:7]
    return render(request, 'axf/home.html', {"title": "主页","wheels":wheelslist,"navs":navlist,"mustbuyList":mustbuylist,"mianmiList":mianmilist})


def market(request, categoryid, cid, sortid):
    leftSlider = FoodTypes.objects.all()

    if cid == '0':
        productList = Goods.objects.filter(categoryid=categoryid)
    else:
        productList = Goods.objects.filter(categoryid=categoryid,childcid = cid)

    # 排序
    if sortid == '1':
        productList = productList.order_by("productnum")
    elif sortid == '2':
        productList = productList.order_by("price")
    elif sortid == '3':
        productList = productList.order_by("-price")

    group = leftSlider.get(typeid = categoryid)
    childList = []
    # 全部分类:0#进口水果:103534#国产水果:103533
    childnames = group.childtypenames
    arr1 = childnames.split("#")
    for str in arr1:
        # 全部分类:0
        arr2 = str.split(":")
        obj = {"childName":arr2[0],"childId":arr2[1]}
        childList.append(obj)

    cartlist = []
    token = request.session.get("token")
    if token:
        user = User.objects.get(userToken = token)
        cartlist = Cart.objects.filter(userAccount = user.userAccount)

    for p in productList:
        for c in cartlist:
            if p.productid == c.productid:
                p.num = c.productnum
                continue

    return render(request, 'axf/market.html', {"title":"闪送超市","leftSlider":leftSlider,"productList":productList,
                                               "childList":childList,"categoryid":categoryid,"cid":cid})



def cart(request):
    cartslist = []
    token = request.session.get("token")
    if token != None:
        user = User.objects.get(userToken=token)
        cartslist = Cart.objects.filter(userAccount = user.userAccount)


    return render(request, 'axf/cart.html', {"title":"购物车","cartslist":cartslist})


def changecart(request,flag):
    #判断用户是否登录
    token = request.session.get("token")
    print("********")
    if token ==None:
        #注意如果是ajax发起的请求不可以用重定向return redirect("/login/") 必须要用JsonResponse
        return JsonResponse({"data":-1,"status":"error"})
    productid = request.POST.get("productid")
    products = Goods.objects.filter(productid = productid)
    product = products[0]
    user = User.objects.get(userToken = token)
    c = None
    if flag == '0':
        if product.storenums == 0:
            return JsonResponse({"data": -2, "status": "error"})
        carts = Cart.objects.filter(userAccount = user.userAccount)
        c = None
        if carts.count() == 0:
            # 直接增加一条订单
            c = Cart.createcart(user.userAccount,productid,1,product.price,True,product.productimg,product.productlongname,False)
            c.save()
            pass
        else:
            try:
                c = carts.get(productid = productid)
                #修改数量和价格
                c.productnum += 1
                c.productprice = "%.2f"%(float(product.price) * c.productnum)
                c.save()
            except Cart.DoesNotExist as e:
                # 直接增加一条订单
                c = Cart.createcart(user.userAccount, productid, 1, product.price, True, product.productimg,product.productlongname, False)
                c.save()
        #库存减一
        product.storenums -= 1
        product.save()
        return JsonResponse({"data":c.productnum, "price":c.productprice,"status":"success"})
    elif flag == '1':
        carts = Cart.objects.filter(userAccount = user.userAccount)
        c = None
        if carts.count() == 0:
            return JsonResponse({"data":-2,"status":"error"})
        else:
            try:
                c = carts.get(productid = productid)
                #修改数量和价格
                c.productnum -= 1
                c.productprice = "%.2f"%(float(product.price) * c.productnum)
                if c.productnum == 0:
                    c.delete()
                else:
                    c.save()
            except Cart.DoesNotExist as e:
                return JsonResponse({"data": -2, "status": "error"})
        #库存减一
        product.storenums += 1
        product.save()
        return JsonResponse({"data":c.productnum, "price":c.productprice,"status":"success"})
    elif flag == '2':
        carts = Cart.objects.filter(userAccount=user.userAccount)
        c = carts.get(productid=productid)
        c.isChose = not c.isChose
        c.save()
        str = ""
        if c.isChose:
            str = "√"
        return JsonResponse({"data": str, "status": "success"})






def mine(request):
    username = request.session.get("username","未登录")
    return render(request, 'axf/mine.html', {"title": "我的","username":username})

from .forms.login import LoginForm
from django.http import HttpResponse,JsonResponse
def login(request):
    if request.method == "POST":
        f = LoginForm(request.POST)
        if f.is_valid():
            # 信息格式没多大问题，验证账号和密码的正确性
            nameid = f.cleaned_data["username"]
            pswd = f.cleaned_data["passwd"]
            try:
                user = User.objects.get(userAccount = nameid)
                if user.userPasswd != pswd:
                    return redirect('/login/')
            except User.DoesNotExist as e:
                return redirect('/login/')

            #登陆成功
            token = time.time() + random.randrange(1, 100000)
            user.userToken = str(token)
            user.save()
            request.session["username"] = user.userName
            request.session["token"] = user.userToken
            return redirect('/mine/')
        else:
            return render(request, 'axf/login.html', {"title": "登陆", "form": f,"error":f.errors})
    else:
        f = LoginForm()
        return render(request, 'axf/login.html', {"title": "登陆","form":f})


#注册
from django.conf import settings
def register(request):
    if request.method == "POST":
        userAccount = request.POST.get("userAccount")
        userPasswd  = request.POST.get("userPass")
        userName    = request.POST.get("userName")
        userPhone   = request.POST.get("userPhone")
        userAdderss = request.POST.get("userAdderss")
        userRank    = 0
        token = time.time() + random.randrange(1, 100000)
        userToken = str(token)
        f = request.FILES["userImg"]
        userImg = os.path.join(settings.MDEIA_ROOT, userAccount + ".png")
        with open(userImg, "wb") as fp:
            for data in f.chunks():
                fp.write(data)

        user = User.createuser(userAccount,userPasswd,userName,userPhone,userAdderss,userImg,userRank,userToken)
        user.save()

        request.session["username"] = userName
        request.session["token"] = userToken

        return redirect('/mine/')
    else:
        return render(request, 'axf/register.html', {"title":"注册"})

def checkuserid(request):
    userid = request.POST.get("userid")
    try:
        user = User.objects.get(userAccount = userid)
        return JsonResponse({"data":"该用户已经被注册","status":"error"})
    except User.DoesNotExist as e:
        return JsonResponse({"data":"可以注册","status":"success"})

# 退出登陆
from django.contrib.auth import logout
def quit(request):
    logout(request)
    return redirect('/mine/')


def saveorder(request):
    # 判断用户是否登录
    token = request.session.get("token")
    if token == None:
        return JsonResponse({"data":-1, "status":"error"})

    user = User.objects.get(userToken=token)
    carts = Cart.objects.filter(isChose = True)
    if carts.count() == 0:
        return JsonResponse({"data": -1, "status": "error"})

    oid = time.time() + random.randrange(1, 10000)
    oid = "%d"%oid
    o = Order.createorder(oid,user.userAccount,0)
    o.save()
    for item in carts:
        item.isDelete = True
        item.orderid = oid
        item.save()
    return JsonResponse({"status": "success"})


def bridgr(request):
    if request.method == "POST":
        data = request.POST.get("tempdata")
        datalist = str(data).split('/')
        dataid = datalist[-4]
        print("dataid=%s"%dataid)
        return JsonResponse({"status": "success","currentpageid":dataid})