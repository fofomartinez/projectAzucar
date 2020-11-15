from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import AreaForm, TContraForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Tipo_Contrato


class TipoContratoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Tipo_Contrato
    template_name = 'tipocontrato/list.html'
    permission_required = 'view_tipo_contrato'

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
                for i in Tipo_Contrato.objects.all():
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
        context['title'] = 'Listado de tipos de contrato'
        context['create_url'] = reverse_lazy('erp:tipo_contrato_create')
        context['list_url'] = reverse_lazy('erp:tipo_contrato_list')
        context['entity'] = 'tipo_contrato'
        return context


class TipoContratoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Tipo_Contrato
    form_class = TContraForm
    template_name = 'tipocontrato/create.html'
    success_url = reverse_lazy('erp:tipo_contrato_list')
    permission_required = 'add_tipo_contrato'
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
        context['title'] = 'Creación un tipo de contrato'
        context['entity'] = 'Tipos de contrato'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class TipoContratoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Tipo_Contrato
    form_class = TContraForm
    template_name = 'tipocontrato/create.html'
    success_url = reverse_lazy('erp:tipo_contrato_list')
    permission_required = 'change_tipo_contrato'
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
        context['title'] = 'Edición de un tipo de contrato'
        context['entity'] = 'Tipos de contrato'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class TipoContratoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Tipo_Contrato
    template_name = 'tipocontrato/delete.html'
    success_url = reverse_lazy('erp:tipo_contrato_list')
    permission_required = 'delete_tipo_contrato'
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
        context['title'] = 'Eliminación de un tipo de contrato'
        context['entity'] = 'Tipos de contrato'
        context['list_url'] = self.success_url
        return context