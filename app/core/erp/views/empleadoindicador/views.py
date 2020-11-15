from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import IngresoIndicadorForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Ingreso_Indicadores


class EmpleadoIndicadorListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Ingreso_Indicadores
    template_name = 'empleadoindicador/list.html'
    permission_required = 'view_ingreso_indicadores'

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
                for i in Ingreso_Indicadores.objects.all():
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
        context['title'] = 'Ingreso de indicadores'
        context['create_url'] = reverse_lazy('erp:empleadoindicador_create')
        context['list_url'] = reverse_lazy('erp:empleadoindicador_list')
        context['entity'] = 'Ingresos'
        return context


class EmpleadoIndicadorCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Ingreso_Indicadores
    form_class = IngresoIndicadorForm
    template_name = 'empleadoindicador/create.html'
    success_url = reverse_lazy('erp:empleadoindicador_list')
    permission_required = 'add_ingreso_indicadores'
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
        context['title'] = 'Registros de indicadores'
        context['entity'] = 'Ingresos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class EmpleadoIndicadorUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Ingreso_Indicadores
    form_class = IngresoIndicadorForm
    template_name = 'empleadoindicador/create.html'
    success_url = reverse_lazy('erp:empleadoindicador_list')
    permission_required = 'change_ingreso_indicadores'
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
        context['title'] = 'Edición de indicadores'
        context['entity'] = 'Ingresos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context

class EmpleadoIndicadoreDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Ingreso_Indicadores
    template_name = 'empleadoindicador/delete.html'
    success_url = reverse_lazy('erp:empleadoindicador_list')
    permission_required = 'delete_ingreso_indicadores'
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
        context['title'] = 'Eliminación de registro de indicadores'
        context['entity'] = 'Puestos'
        context['list_url'] = self.success_url
        return context




