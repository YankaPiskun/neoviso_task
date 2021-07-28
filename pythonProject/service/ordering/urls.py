from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    path('about', views.about, name='about'),
    path('create', views.create, name='create'),
    path('client', views.client, name='client'),
    path('<int:pk>', views.OrderDetailView.as_view(), name='order-detail'),
    path('<int:pk>/update', views.OrdersUpdateView.as_view(), name='order-update'),
    path('<int:pk>/delete', views.OrdersDeleteView.as_view(), name='order-delete')


]
