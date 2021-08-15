from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm
from django.views.generic import DetailView, UpdateView, DeleteView
# Create your views here.

def index(request):
    return render(request, 'main/index.html', {'title': 'Главная страница!!'})


def about(request):
    return render(request, 'main/about.html')


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


