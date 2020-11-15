from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import BodegaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Bodega


class BodegaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Bodega
    template_name = 'bodega/list.html'
    permission_required = 'view_bodega'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                position = 1
                for i in Bodega.objects.all():
                    item = i.toJSON()
                    item['position'] = position
                    data.append(item)
                    position += 1
                    # data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de bodegas'
        context['create_url'] = reverse_lazy('erp:bodega_create')
        context['list_url'] = reverse_lazy('erp:bodega_list')
        context['entity'] = 'Bodegas'
        return context


class BodegaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Bodega
    form_class = BodegaForm
    template_name = 'bodega/create.html'
    success_url = reverse_lazy('erp:bodega_list')
    permission_required = 'add_bodega'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'add':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de bodegas'
        context['entity'] = 'Bodegas'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class BodegaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Bodega
    form_class = BodegaForm
    template_name = 'bodega/create.html'
    success_url = reverse_lazy('erp:bodega_list')
    permission_required = 'change_bodega'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'edit':
                form = self.get_form()
                data = form.save()
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de bodegas'
        context['entity'] = 'Bodegas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class BodegaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Bodega
    template_name = 'bodega/delete.html'
    success_url = reverse_lazy('erp:bodega_list')
    permission_required = 'delete_bodega'
    url_redirect = success_url

    def dispatch(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            self.object.delete()
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Eliminación de bodegas'
        context['entity'] = 'Bodegas'
        context['list_url'] = self.success_url
        return context