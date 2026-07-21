from django.shortcuts import get_object_or_404
from django.views.generic import CreateView, DeleteView, ListView, UpdateView
from django.urls import reverse_lazy

from .models import Contact


class ContactListView(ListView):
    model = Contact
    template_name = 'contact/contact_list.html'
    context_object_name = 'contacts'

    def get_queryset(self):
        queryset = super().get_queryset()
        query = self.request.GET.get('q', '').strip()
        if query:
            queryset = queryset.filter(name__icontains=query)
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['query'] = self.request.GET.get('q', '')
        return context


class ContactCreateView(CreateView):
    model = Contact
    template_name = 'contact/contact_form.html'
    fields = ['name', 'email', 'phone', 'information']
    success_url = reverse_lazy('contact_list')


class ContactUpdateView(UpdateView):
    model = Contact
    template_name = 'contact/contact_form.html'
    fields = ['name', 'email', 'phone', 'information']
    success_url = reverse_lazy('contact_list')


class ContactDeleteView(DeleteView):
    model = Contact
    template_name = 'contact/contact_confirm_delete.html'
    success_url = reverse_lazy('contact_list')

    def get_object(self, queryset=None):
        return get_object_or_404(Contact, pk=self.kwargs['pk'])


contact_list = ContactListView.as_view()
contact_create = ContactCreateView.as_view()
contact_update = ContactUpdateView.as_view()
contact_delete = ContactDeleteView.as_view()
