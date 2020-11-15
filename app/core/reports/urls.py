from django.urls import path

from core.reports.views import ReportSaleView, ReportPedidoView

urlpatterns = [
    # url para reportes
    path('sale/', ReportSaleView.as_view(), name='sale_report'),
    path('pedidos/', ReportPedidoView.as_view(), name='pedidos_report'),
]