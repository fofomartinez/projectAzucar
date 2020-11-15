from django.db.models import Sum
from django.db.models.functions import Coalesce
from django.http import JsonResponse
from django.urls import reverse_lazy
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from core.erp.models import Venta, Pedido, DetPedido
from core.reports.forms import ReportForm


class ReportSaleView(TemplateView):
    template_name = 'sale/report.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                # todos los datos
                search = Venta.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date]) #date range es para las fechas rangos
                for s in search:
                    # mandar a manera de array
                    data.append([
                        s.id,
                        s.cli.names,
                        s.date_joined.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])

                # variables con sumatorias
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'),0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'),0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'),0)).get('r')

                data.append([
                    '  ',
                    '  ',
                    '  ',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),

                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Ventas'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('sale_report')
        context['form'] = ReportForm()
        return context

class ReportPedidoView(TemplateView):
    template_name = 'sale/pedidos.html'

    @method_decorator(csrf_exempt)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        data = {}
        try:
            action = request.POST['action']
            if action == 'search_report':
                data = []
                start_date = request.POST.get('start_date', '')
                end_date = request.POST.get('end_date', '')
                # todos los datos
                search = Pedido.objects.all()
                if len(start_date) and len(end_date):
                    search = search.filter(date_joined__range=[start_date, end_date]) #date range es para las fechas rangos
                for s in search:
                    # mandar a manera de array
                    data.append([
                        s.id,
                        s.cliente.nombre,
                        s.fecha.strftime('%Y-%m-%d'),
                        format(s.subtotal, '.2f'),
                        format(s.iva, '.2f'),
                        format(s.total, '.2f'),
                    ])

                # variables con sumatorias
                subtotal = search.aggregate(r=Coalesce(Sum('subtotal'),0)).get('r')
                iva = search.aggregate(r=Coalesce(Sum('iva'),0)).get('r')
                total = search.aggregate(r=Coalesce(Sum('total'),0)).get('r')

                data.append([
                    '  ',
                    '  ',
                    '  ',
                    format(subtotal, '.2f'),
                    format(iva, '.2f'),
                    format(total, '.2f'),

                ])
            else:
                data['error'] = 'Ha ocurrido un error'
        except Exception as e:
            data['error'] = str(e)
        return JsonResponse(data, safe=False)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Reporte de Pedidos'
        context['entity'] = 'Reportes'
        context['list_url'] = reverse_lazy('erp:pedido_list')
        context['form'] = ReportForm()
        return context