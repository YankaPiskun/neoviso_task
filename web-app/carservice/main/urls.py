from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('order', views.order, name='order'),
    path('create', views.create, name='create'),
    path('<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/update', views.OrderUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete', views.OrderDeleteView.as_view(), name='order-delete')
]