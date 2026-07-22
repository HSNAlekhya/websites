from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, DetailView, ListView, UpdateView

from .forms import OrderForm
from .models import Order


class OrderListView(ListView):
	model = Order
	context_object_name = 'orders'
	template_name = 'order/order_list.html'


class OrderDetailView(DetailView):
	model = Order
	template_name = 'order/order_detail.html'


class OrderCreateView(CreateView):
	model = Order
	form_class = OrderForm
	template_name = 'order/order_form.html'


class OrderUpdateView(UpdateView):
	model = Order
	form_class = OrderForm
	template_name = 'order/order_form.html'


class OrderDeleteView(DeleteView):
	model = Order
	template_name = 'order/order_confirm_delete.html'
	success_url = reverse_lazy('order-list')
