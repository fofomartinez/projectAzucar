from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from xhtml2pdf import pisa

from core.erp.forms import ContratoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from core.erp.models import Contrato
from django.conf import settings
import json
import os


class ContratoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Contrato
    template_name = 'contrato/list.html'
    permission_required = 'view_contrato'

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
                for i in Contrato.objects.all():
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
        context['title'] = 'Listado de Contratos'
        context['create_url'] = reverse_lazy('erp:contrato_create')
        context['list_url'] = reverse_lazy('erp:contrato_list')
        context['entity'] = 'Contratos'
        return context


class ContratoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contrato/create.html'
    success_url = reverse_lazy('erp:contrato_list')
    permission_required = 'add_contrato'
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
        context['title'] = 'Creación un contrato'
        context['entity'] = 'Contratos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        return context


class ContratoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Contrato
    form_class = ContratoForm
    template_name = 'contrato/create.html'
    success_url = reverse_lazy('erp:contrato_list')
    permission_required = 'change_contrato'
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
        context['title'] = 'Edición de contratos'
        context['entity'] = 'Contratos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        return context


class ContratoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Contrato
    template_name = 'contrato/delete.html'
    success_url = reverse_lazy('erp:contrato_list')
    permission_required = 'delete_contrato'
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
        context['title'] = 'Eliminación de un contrato'
        context['entity'] = 'Contratos'
        context['list_url'] = self.success_url
        return context

class ImpresionContratoPdfView(View):


    def link_callback(self, uri, rel):
        """
        Convert HTML URIs to absolute system paths so xhtml2pdf can access those
        resources
        """
        # use short variable names
        sUrl = settings.STATIC_URL  # Typically /static/
        sRoot = settings.STATIC_ROOT  # Variable para recoopilar archivos estaticos
        mUrl = settings.MEDIA_URL  # Typically /static/media/
        mRoot = settings.MEDIA_ROOT  # Typically /home/userX/project_static/media/

        # convert URIs to absolute system paths
        if uri.startswith(mUrl):
            path = os.path.join(mRoot, uri.replace(mUrl, ""))
        elif uri.startswith(sUrl):
            path = os.path.join(sRoot, uri.replace(sUrl, ""))
        else:
            return uri  # handle absolute uri (ie: http://some.tld/foo.png)

        # make sure that file exists
        if not os.path.isfile(path):
            raise Exception(
                'media URI must start with %s or %s' % (sUrl, mUrl)
            )
        return path

    def get(self, request, *args, **kwargs):
        try:
            template = get_template('contrato/contrato.html')
            context = {
                'contrato': Contrato.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Industrias Azucareras de Guatemala', 'Dirección': 'Fray B. De las Casas, AV.'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Contrato de trabajo.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:contrato_list'))

