from django.urls import path
from . import views

urlpatterns = [
    path('orderinfo/', views.OrderDetailView.as_view()),
    path('submittext/', views.SubmitText.as_view()),

    path('ongoing/', views.OnGoingView.as_view()),
    path('check/', views.CheckView.as_view()),
    path('notstart/', views.notStartView.as_view()),
    path('reject/', views.RejectView.as_view()),
    path('finish/', views.FinishView.as_view()),
]
