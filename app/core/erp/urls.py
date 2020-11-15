from django.urls import path

from core.erp.views.area.views import *
from core.erp.views.bodega.views import *
from core.erp.views.category.views import *
from core.erp.views.client.views import *
from core.erp.views.contrato.views import *
from core.erp.views.dashboard.views import *
from core.erp.views.empleado.views import *
from core.erp.views.empleadoindicador.views import *
from core.erp.views.indicador.views import *
from core.erp.views.pedido.views import *
from core.erp.views.product.views import *
from core.erp.views.puesto.views import *
from core.erp.views.sales.views import SaleCreateView, SaleListView, SaleDeleteView, SaleUpdateView, SaleInvoicePdfView
from core.erp.views.tests.views import TestView
from core.erp.views.tipocontrato.views import *

app_name = 'erp'

urlpatterns = [
    # categorias de producto
    path('category/list/', CategoryListView.as_view(), name='category_list'),
    path('category/add/', CategoryCreateView.as_view(), name='category_create'),
    path('category/update/<int:pk>/', CategoryUpdateView.as_view(), name='category_update'),
    path('category/delete/<int:pk>/', CategoryDeleteView.as_view(), name='category_delete'),
    # clientes
    path('client/list/', ClientListView.as_view(), name='client_list'),
    path('client/add/', ClientCreateView.as_view(), name='client_create'),
    path('client/update/<int:pk>/', ClientUpdateView.as_view(), name='client_update'),
    path('client/delete/<int:pk>/', ClientDeleteView.as_view(), name='client_delete'),
    # producto
    path('product/list/', ProductListView.as_view(), name='product_list'),
    path('product/add/', ProductCreateView.as_view(), name='product_create'),
    path('product/update/<int:pk>/', ProductUpdateView.as_view(), name='product_update'),
    path('product/delete/<int:pk>/', ProductDeleteView.as_view(), name='product_delete'),
    # inicio
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
    # test
    path('test/', TestView.as_view(), name='test'),
    # ventas
    path('sale/list/', SaleListView.as_view(), name='sale_list'),
    path('sale/add/', SaleCreateView.as_view(), name='sale_create'),
    path('sale/delete/<int:pk>/', SaleDeleteView.as_view(), name='sale_delete'),
    path('sale/update/<int:pk>/', SaleUpdateView.as_view(), name='sale_update'),
    path('sale/invoice/pdf/<int:pk>/', SaleInvoicePdfView.as_view(), name='sale_update'),

    # areas
    path('area/list/', AreaListView.as_view(), name='area_list'),
    path('area/add/', AreaCreateView.as_view(), name='area_create'),
    path('area/update/<int:pk>/', AreaUpdateView.as_view(), name='area_update'),
    path('area/delete/<int:pk>/', AreaDeleteView.as_view(), name='area_delete'),

    # Empleados
    path('empleado/list/', EmpleadoListView.as_view(), name='empleado_list'),
    path('empleado/add/', EmpleadoCreateView.as_view(), name='empleado_create'),
    path('empleado/update/<int:pk>/', EmpleadoUpdateView.as_view(), name='empleado_update'),
    path('empleado/delete/<int:pk>/', EmpleadoDeleteView.as_view(), name='empleado_delete'),


    # tipo_contrato
    path('tipo_contrato/list/', TipoContratoListView.as_view(), name='tipo_contrato_list'),
    path('tipo_contratoo/add/', TipoContratoCreateView.as_view(), name='tipo_contrato_create'),
    path('tipo_contrato/update/<int:pk>/', TipoContratoUpdateView.as_view(), name='tipo_contrato_update'),
    path('tipo_contrato/delete/<int:pk>/', TipoContratoDeleteView.as_view(), name='tipo_contrato_delete'),

    # puestos
    path('puesto/list/', PuestoListView.as_view(), name='puesto_list'),
    path('puesto/add/', PuestoCreateView.as_view(), name='puesto_create'),
    path('puesto/update/<int:pk>/', PuestoUpdateView.as_view(), name='puesto_update'),
    path('puesto/delete/<int:pk>/', PuestoDeleteView.as_view(), name='puesto_delete'),

    # bodegas
    path('bodega/list/', BodegaListView.as_view(), name='bodega_list'),
    path('bodega/add/', BodegaCreateView.as_view(), name='bodega_create'),
    path('bodega/update/<int:pk>/', BodegaUpdateView.as_view(), name='bodega_update'),
    path('bodega/delete/<int:pk>/', BodegaDeleteView.as_view(), name='bodega_delete'),

    # indicador
    path('indicador/list/', IndicadorListView.as_view(), name='indicador_list'),
    path('indicador/add/',IndicadorCreateView.as_view(), name='indicador_create'),
    path('indicador/update/<int:pk>/', IndicadorUpdateView.as_view(), name='indicador_update'),
    path('indicador/delete/<int:pk>/', IndicadorDeleteView.as_view(), name='indicador_delete'),

    # ingreso de indicadores
    path('empleadoindicador/list/', EmpleadoIndicadorListView.as_view(), name='empleadoindicador_list'),
    path('empleadoindicador/add/', EmpleadoIndicadorCreateView.as_view(), name='empleadoindicador_create'),
    path('empleadoindicador/update/<int:pk>/', EmpleadoIndicadorUpdateView.as_view(), name='empleadoindicador_update'),
    path('empleadoindicador/delete/<int:pk>/', EmpleadoIndicadoreDeleteView.as_view(), name='empleadoindicador_delete'),

    # contratos
    path('contrato/list/', ContratoListView.as_view(), name='contrato_list'),
    path('contrato/add/', ContratoCreateView.as_view(), name='contrato_create'),
    path('contrato/update/<int:pk>/', ContratoUpdateView.as_view(), name='contrato_update'),
    path('contrato/delete/<int:pk>/', ContratoDeleteView.as_view(), name='contrato_delete'),
    path('contrato/impresion/pdf/<int:pk>/', ImpresionContratoPdfView.as_view(), name='contrato_update'),


# Pedidos
    path('pedido/list/', PedidoListView.as_view(), name='pedido_list'),
    path('pedido/add/', PedidoCreateView.as_view(), name='pedido_create'),
    path('pedido/delete/<int:pk>/', PedidoDeleteView.as_view(), name='pedido_delete'),
    path('pedido/update/<int:pk>/', PedidoUpdateView.as_view(), name='pedido_update'),
    path('pedido/invoice/pdf/<int:pk>/', PedidoInvoicePdfView.as_view(), name='pedido_update'),

]
