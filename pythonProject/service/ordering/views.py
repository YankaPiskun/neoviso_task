
from django.shortcuts import render, redirect
from .models import Orders
from .models import Clients
from .forms import OrdersForm
from django.views.generic import DetailView, UpdateView, DeleteView


def index(request):
    orderss = Orders.objects.all()
    return render(request, 'ordering/index.html', {'title': 'Главная страница сайта', 'orderss': orderss})


def about(request):
    return render(request, 'ordering/about.html')


def client(request):
    clientss = Clients.objects.all()
    return render(request, 'ordering/client.html', {'clientss': clientss})


class OrderDetailView(DetailView):
    model = Orders
    template_name = 'ordering/details_view.html'
    context_object_name = 'ord'


class OrdersUpdateView(UpdateView):
    model = Orders
    template_name = 'ordering/create.html'
    form_class = OrdersForm


class OrdersDeleteView(DeleteView):
    model = Orders
    success_url = '/'
    template_name = 'ordering/orders-delete.html'





def create(request):
    error = ''
    if request.method == 'POST':
        form = OrdersForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect('home')
        else:
            error = 'Форма была неверной'


    form = OrdersForm()
    context = {
        'form': form,
        'error': error
    }
    return render(request, 'ordering/create.html', context)

