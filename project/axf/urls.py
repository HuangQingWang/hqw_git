from django.conf.urls import url
from . import views
urlpatterns = [

    url(r'^initdatabases/$', views.initdatabases,name="initdatabases"),

    url(r'^home/$', views.home,name="home"),
    url(r'^market/(\d+)/(\d+)/(\d+)/$', views.market, name="market"),
    url(r'^cart/$', views.cart, name="cart"),
    url(r'^mine/$', views.mine, name="mine"),

    url(r'^login/$', views.login, name="login"),
    url(r'^register/$', views.register, name="register"),
    # 验证账号是否被注册
    url(r'^checkuserid/$', views.checkuserid, name="checkuserid"),
    url(r'^quit/$', views.quit, name="quit"),

    url(r'^changecart/(\d+)/$', views.changecart, name="changecart"),

    # 下订单
    url(r'^saveorder/$', views.saveorder, name="saveorder"),

    url(r'^bridgr/$', views.bridgr, name="bridgr"),


]
