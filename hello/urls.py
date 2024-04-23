"""Inventory URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from .views import abaixo_est_min_view, add_produto_pedido_view, dashboard_view, detalhes_pedido_view, editar_fornecedor_view, editar_pedido_view, editar_produto_view, fornecedores_view, login_view, home_view, pedidos_view, produtos_view, logout_view, relatorio_consumo_view, remover_fornecedor_view, remover_produto_pedido_view, entradas_view, add_entrada_view, saidas_view, add_saida_view

urlpatterns = [
    path('', login_view, name='login'),
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
    path('home/', home_view, name='home'),
    path('produtos/', produtos_view, name='produtos'),
    path('produto/<int:produto_id>/editar/', editar_produto_view, name='editar_produto'),
    path('pedidos/', pedidos_view, name='pedidos'),
    path('entradas/', entradas_view, name='entradas'),
    path('add_entrada/', add_entrada_view, name='add_entrada'),
    path('saidas/', saidas_view, name='saidas'),
    path('add_saida/', add_saida_view, name='add_saida'),
    path('pedido/<int:pedido_id>/adicionar_produto/', add_produto_pedido_view, name='add_produto_pedido'),
    path('pedido/<int:pedido_id>/', detalhes_pedido_view, name='detalhes_pedido'),
    path('pedido/<int:pedido_id>/produto/<int:produto_pedido_id>/remover/', remover_produto_pedido_view, name='remover_produto_pedido'),
    path('pedido/<int:pedido_id>/editar/', editar_pedido_view, name='editar_pedido'),
    path('fornecedores/', fornecedores_view, name='fornecedores'),
    path('fornecedores/editar/<int:fornecedor_id>/', editar_fornecedor_view, name='editar_fornecedor'),
    path('fornecedores/remover/<int:fornecedor_id>/',remover_fornecedor_view, name='remover_fornecedor'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('abaixo_est_min/', abaixo_est_min_view, name='abaixo_est_min'),
    path('relatorio_consumo/', relatorio_consumo_view, name='relatorio_consumo'),
]



