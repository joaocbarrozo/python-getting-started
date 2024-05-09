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
    quantidade = models.PositiveIntegerField(default=0)
    estoque_minimo = models.PositiveIntegerField(default=0)
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE, default="")
    local = models.ForeignKey(LocalPrateleira, on_delete=models.CASCADE, default="")
    
    def __str__(self):
        return self.nome

class Fornecedor(models.Model):
    cnpj = models.CharField(max_length=16, unique=True)
    razao_social = models.CharField(max_length=255)
    nome = models.CharField(max_length=255)
    fone = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    contato = models.CharField(max_length=64, blank=True, null=True)
    estado = models.CharField(max_length=4, blank=True, null=True)
    municipio = models.CharField(max_length=32, blank=True, null=True)
    bairro = models.CharField(max_length=32, blank=True, null=True)
    endereco = models.CharField(max_length=128, blank=True, null=True)
    numero = models.CharField(max_length=8, blank=True, null=True)
    cep = models.CharField(max_length=16, blank=True, null=True)
    def __str__(self):
        return self.nome

class Entrada(models.Model):
    TIPO = (
        ('C', 'COMPRA'),
        ('D', 'DOAÇÃO')
    )
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    tipo = models.CharField(max_length=16, choices=TIPO)
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    quantidade = models.PositiveIntegerField()
    preco_unitario = models.DecimalField(max_digits=6, decimal_places=2)
    criado_em = models.DateTimeField(auto_now_add=True)
    #usuario = models.ForeignKey(User.username, on_delete=models.CASCADE)
 
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
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    
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



class Compra(models.Model):#Dados extraidos via XML dos dados das NF-es
    STATUS = (
        ('E', 'Entregue'),
        ('A', 'Aguardando'),
        ('C', 'Cancelada')
    )    
    numero_id = models.CharField(max_length=64, unique=True)#Identificador da NF-e de 44 digitos
    numero = models.CharField(max_length=16)#Numero da NF-e
    data_emissao = models.DateTimeField()
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE)
    criado_em = models.DateTimeField(auto_now_add=True)
    recebida_em = models.DateTimeField()
    status = models.CharField(max_length=20,choices=STATUS)
    #solicitante = models.ForeignKey(User, on_delete=models.CASCADE) 

class ItemNF(models.Model):#Dados extraidos via XML
    codigo = models.CharField(max_length=32)#Codigo que consta no xml
    descricao = models.CharField(max_length=255)
    unidade = models.CharField(max_length=8)
    quantidade = models.CharField(max_length=32)
    preco_unitario = models.CharField(max_length=32)
    valot_total = models.CharField(max_length=32)
    entrada = models.CharField(max_length=2)
    data_importacao = models.DateTimeField(auto_now=True)




# Create your models here.
