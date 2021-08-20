from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from django.views.generic import DetailView, UpdateView, DeleteView
from rest_framework.response import Response
from rest_framework.views import APIView
from .serializers import OrderSerializer
from rest_framework import status
from django.http import Http404



# Create your views here.


def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница!!'})


def about(request):
    return render(request, 'main/about.html')


def employees(request):
    return render(request, 'main/employees.html')


def services(request):
    return render(request, 'main/services.html')


def order(request):
    orders = Order.objects.all()
    return render(request, "main/order.html", {'title': 'Заказы', 'orders': orders})


def create(request):
    error = ''
    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order')
        else:
            error = 'Форма была не верной'

    form = OrderForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', data)


class OrderDetailView(DetailView):
    model = Order
    template_name = 'main/details_view.html'
    context_object_name = 'order'


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'main/create.html'

    form_class = OrderForm


class OrderDeleteView(DeleteView):
    model = Order
    success_url = '/order'
    template_name = 'main/order-delete.html'


class OrderApiView(APIView):
    def get(self, request):
        orders = Order.objects.all()
        serializer = OrderSerializer(orders, many=True)
        return Response({"orders": serializer.data})

    def post(self, request):
        serializer = OrderSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class OrderApiDetail(APIView):
    def get_object(self, pk):
        try:
            return Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        orders = self.get_object(pk)
        serializer = OrderSerializer(orders)
        return Response(serializer.data)

    def put(self, request, pk):
        orders = self.get_object(pk)
        serializer = OrderSerializer(orders, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        orders = self.get_object(pk)
        orders.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)