from django.urls import path
from .views import PaymentView,PaymentCurdView


urlpatterns=[
    path('',PaymentView.as_view(),name='payment'),
    path('curd/<str:pk>/',PaymentCurdView.as_view(),name='payment Curd'),
]