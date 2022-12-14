from django.urls import path

from users import views

urlpatterns = [
    # 登录
    path('login/', views.Login.as_view()),
    # 创建账号
    path('create/', views.CreateUser.as_view()),
    # 获取菜单
    # path('menu/', views.MenuView.as_view()),
    # 获取角色
    path('roles/', views.RoleView.as_view()),
    # path('permission/', views.PerssionView.as_view()),
    # 根据角色id获取该角色下所有用户
    path('getuser/', views.getUserView.as_view()),
]
