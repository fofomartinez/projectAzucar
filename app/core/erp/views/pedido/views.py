import json
import os
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template.loader import get_template
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
# from psycopg2.extensions import JSON
from xhtml2pdf import pisa
from django.conf import settings

from core.erp.forms import PedidoForm
from core.erp.mixins import ValidatePermissionRequiredMixin
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View

from core.erp.models import Pedido, Producto, DetPedido

class PedidoListView(LoginRequiredMixin, ValidatePermissionRequiredMixin, ListView):
    model = Pedido
    template_name = 'pedido/list.html'
    permission_required = 'view_pedido'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'searchdata':
                data = []
                for i in Pedido.objects.all():
                    data.append(i.toJSON())
            elif action == 'search_details_prod':
                data = []
                for i in DetPedido.objects.filter(pedido_id=request.POST['id']):
                    data.append(i.toJSON())
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Listado de Pedidos'
        context['create_url'] = reverse_lazy('erp:pedido_create')
        context['list_url'] = reverse_lazy('erp:pedido_list')
        context['entity'] = 'Pedidos'
        return context

class PedidoCreateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, CreateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido/create.html'
    success_url = reverse_lazy('erp:pedido_list')
    permission_required = 'add_pedido'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    # item['value'] = i.name esto #esto es para ui buscador
                    item['text'] = i.name #esto esto es para ui buscador
                    data.append(item)
            elif action == 'add':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # vents = json.loads(request.POST['vents'])

                    ped = Pedido()
                    ped.fecha = vents['date_joined']
                    ped.cliente_id = vents['cli']
                    ped.subtotal = float(vents['subtotal'])
                    ped.iva = float(vents['iva'])
                    ped.total = float(vents['total'])
                    ped.save()

                    for i in vents['products']:
                        det = DetPedido()
                        det.pedido_id = ped.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()

                        # para saber que id de venta se esta creando e imprimirla
                    data={'id':ped.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Registro de un pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'add'
        context['det'] = []
        return context

class PedidoUpdateView(LoginRequiredMixin, ValidatePermissionRequiredMixin, UpdateView):
    model = Pedido
    form_class = PedidoForm
    template_name = 'pedido/create.html'
    success_url = reverse_lazy('erp:pedido_list')
    permission_required = 'change_pedido'
    url_redirect = success_url

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_products':
                data = []
                prods = Producto.objects.filter(name__icontains=request.POST['term'])[0:10]
                for i in prods:
                    item = i.toJSON()
                    item['value'] = i.name
                    data.append(item)
            elif action == 'edit':
                with transaction.atomic():
                    vents = json.loads(request.POST['vents'])
                    # sale = Sale.objects.get(pk=self.get_object().id)
                    ped = self.get_object()
                    ped.fecha = vents['date_joined']
                    ped.cliente_id = vents['cli']
                    ped.subtotal = float(vents['subtotal'])
                    ped.iva = float(vents['iva'])
                    ped.total = float(vents['total'])
                    ped.save()
                    # eliminar los productos anteriores

                    ped.detpedido_set.all().delete()
                    for i in vents['products']:
                        det = DetPedido()
                        det.pedido_id = ped.id
                        det.prod_id = i['id']
                        det.cant = int(i['cant'])
                        det.precio = float(i['precio'])
                        det.subtotal = float(i['subtotal'])
                        det.save()
                    # para saber que id de venta se esta creando e imprimirla
                    data = {'id': ped.id}
            else:
                data['error'] = 'No ha ingresado a ninguna opción'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_details_product(self):
        data = []
        try:
            for i in DetPedido.objects.filter(pedido_id=self.get_object().id):
                item = i.prod.toJSON()
                item['cant'] = i.cant
                data.append(item)
        except:
            pass
        return data

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de una pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        context['action'] = 'edit'
        context['det'] = json.dumps(self.get_details_product())
        return context

class PedidoDeleteView(LoginRequiredMixin, ValidatePermissionRequiredMixin, DeleteView):
    model = Pedido
    template_name = 'pedido/delete.html'
    success_url = reverse_lazy('erp:pedido_list')
    permission_required = 'delete_pedido'
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
        context['title'] = 'Eliminación de un pedido'
        context['entity'] = 'Pedidos'
        context['list_url'] = self.success_url
        return context

class PedidoInvoicePdfView(View):

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
            template = get_template('pedido/invoice.html')
            context = {
                'pedido': Pedido.objects.get(pk=self.kwargs['pk']),
                'comp': {'name': 'Indistria Azucarera de Guatemala', 'ruc': '297452-6', 'address': 'Fray B. De las Casas, AV.'},
                'icon': '{}{}'.format(settings.MEDIA_URL, 'logo.png')
            }
            html = template.render(context)
            response = HttpResponse(content_type='application/pdf')
            response['Content-Disposition'] = 'attachment; filename="Pedido.pdf"'
            pisaStatus = pisa.CreatePDF(
                html, dest=response,
                link_callback=self.link_callback
            )
            return response
        except:
            pass
        return HttpResponseRedirect(reverse_lazy('erp:pedido_list'))

