from django.db import models
from django.contrib.auth.models import User

class Setor(models.Model):
    setorNome = models.CharField(max_length=64)
    def __str__(self):
        return self.setorNome
    
class Categoria(models.Model):
    categoriaNome = models.CharField(max_length=64)
    def __str__(self):
        return self.categoriaNome

class LocalPrateleira(models.Model):
    localNome = models.CharField(max_length=64)
    def __str__(self):
        return self.localNome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    quantidade = models.PositiveIntegerField()
    estoque_minimo = models.PositiveIntegerField()
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default="")
    local = models.ForeignKey(LocalPrateleira, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    fone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    def __str__(self):
        return self.nome

class Entrada(models.Model):
    TIPO = (
        ('COMPRA', 'COMPRA'),
        ('DOAÇÃO', 'DOAÇÃO')
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=16, choices=TIPO)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
 
    def __str__(self):
        return self.produto.nome
        
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)   
        self.produto.quantidade += self.quantidade
        self.produto.save()

class Saida(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    setor = models.ForeignKey(Setor, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    criado_em = models.DateTimeField(auto_now_add=True)
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.produto.nome
        
    def save(self, *args, **kwargs):
        if self.quantidade <= self.produto.quantidade:
            super().save(*args, **kwargs)
            self.produto.quantidade -= self.quantidade
            self.produto.save()
        else:
            raise ValueError("Quantidade de saída excede a quantidade disponível do produto.")
     
class Pedido(models.Model):
    STATUS = (
        ('Aberto', 'aberto'),
        ('Realizado', 'realizado'),
        ('Cancelado', 'cancelado')
    )
    produtos = models.ManyToManyField(Produto, through="ProdutoPedido")
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)

class ProdutoPedido(models.Model):
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveBigIntegerField()


class Compra(models.Model):
    STATUS = (
        ('Recebida', 'recebida'),
        ('Não-Recebida', 'não-recebida'),
        ('Cancelada', 'cancelada')
    )    
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE)
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    quantidade = models.PositiveBigIntegerField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS)
    solicitante = models.ForeignKey(User, on_delete=models.CASCADE) 




# Create your models here.
