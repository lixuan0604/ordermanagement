


from django.urls import path
from . import views

urlpatterns = [
    # 判断用户名是否重复
    # path('api/order/',views.OrderView.as_view()),
    path('createmaster', views.CreateMasterOrderView.as_view()),
    path('createsub', views.CreateSubOrderView.as_view()),
    path('getorderlist', views.GetOrderView.as_view()),
    path('assignwriter', views.AssignWriterView.as_view()),
    path('inspect', views.InspectdSubOrderView.as_view()),
    path('downloadorder', views.DownLoadFileView.as_view())
]