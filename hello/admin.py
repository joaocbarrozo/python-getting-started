from django.contrib import admin

from almoxarifado.models import Produto, Fornecedor, ProdutoPedido, Pedido, Categoria, Setor, LocalPrateleira, Entrada, Saida

@admin.register(Produto)
class ProdutoAdmin(admin.ModelAdmin):
    pass

@admin.register(Fornecedor)
class FornecedorAdmin(admin.ModelAdmin):
    pass

@admin.register(ProdutoPedido)
class ProdutoPedidoAdmin(admin.ModelAdmin):
    pass

@admin.register(Pedido)
class PedidoAdmin(admin.ModelAdmin):
    pass

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    pass

@admin.register(Setor)
class SetorAdmin(admin.ModelAdmin):
    pass

@admin.register(LocalPrateleira)
class LocalPrateleiraAdmin(admin.ModelAdmin):
    pass

@admin.register(Entrada)
class EntradaAdmin(admin.ModelAdmin):
    pass

@admin.register(Saida)
class SaidaAdmin(admin.ModelAdmin):
    pass
# Register your models here.
