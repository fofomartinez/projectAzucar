from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from core.erp.forms import AreaForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Area


class AreaListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Area
    template_name = 'area/list.html'
    permission_required = 'view_area'

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
                for i in Area.objects.all():
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
        context['title'] = 'Listado de Areas'
        context['create_url'] = reverse_lazy('erp:area_create')
        context['list_url'] = reverse_lazy('erp:area_list')
        context['entity'] = 'Areas'
        return context


class AreaCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/create.html'
    success_url = reverse_lazy('erp:area_list')
    permission_required = 'add_area'
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
        context['title'] = 'Creación una Categoria'
        context['entity'] = 'Categorias'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class AreaUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Area
    form_class = AreaForm
    template_name = 'area/create.html'
    success_url = reverse_lazy('erp:area_list')
    permission_required = 'change_area'
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
        context['title'] = 'Edición de un area'
        context['entity'] = 'Areas'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class AreaDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Area
    template_name = 'area/delete.html'
    success_url = reverse_lazy('erp:area_list')
    permission_required = 'delete_area'
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
        context['title'] = 'Eliminación de un area'
        context['entity'] = 'Areas'
        context['list_url'] = self.success_url
        return context