from django.shortcuts import get_object_or_404, render, redirect
from .models import Fornecedor, Produto, Pedido, ProdutoPedido, Entrada, Saida
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import FiltroDataForm, FornecedorForm, ProdutoForm, PedidoForm, ProdutoPedidoForm, EntradasForm, SaidasForm
from django.db.models import Q
from datetime import datetime
from django.db.models import Sum, F, Q, Subquery, OuterRef, ExpressionWrapper, FloatField

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home') # replace 'dashboard' with the name of your dashboard view
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')
    
@login_required    
def home_view(request):
    produtos = Produto.objects.all().order_by('nome')
    produtosAtual = produtos.filter(quantidade__gt=0)
    context = {'produtos': produtosAtual}
    return render(request, 'home.html', context)

@login_required    
def abaixo_est_min_view(request):
    produtos = Produto.objects.all().order_by('nome')
    abaixoEstMin = produtos.filter(quantidade__lt=F('estoque_minimo'))
    context = {'produtos': abaixoEstMin}
    return render(request, 'abaixo_est_min.html', context)

@login_required
def relatorio_consumo_view(request):
    saidas = []
    if request.method == 'GET':
        form = FiltroDataForm(request.GET)
        if form.is_valid():
            data_inicial = form.cleaned_data['data_inicial']
            data_final = form.cleaned_data['data_final']

            saidas = (
                Saida.objects.filter(criado_em__range=(data_inicial, data_final))
                .values('produto', 'produto__nome', 'produto__descricao')
                .annotate(quantidade_total=Sum('quantidade')))
            saidas = saidas.order_by('produto__nome')
            
    else:
        form = FiltroDataForm()

    context = {'form': form, 'saidas': saidas}
    return render(request, 'relatorio_consumo.html', context)


@login_required
def dashboard_view(request):
    # Cálculo do valor total em estoque
    valor_total_estoque= 0
    sem_entrada_registrada = 0
    #Seleciona todos os produtos ordenando por nome
    produtos = Produto.objects.all().order_by('nome')
    #Lista de produtos com pelo menos um item em estoque
    produtosAtual = produtos.filter(quantidade__gt=0)
    #Verifica o ultimo preço de cada item em estoque atual
    for produto in produtosAtual:
        ultima_entrada = Entrada.objects.filter(Q(produto=produto) & Q(tipo="COMPRA")
).order_by('-criado_em').first()
        if ultima_entrada and ultima_entrada.preco_unitario > 0:
            valor_unitario = ultima_entrada.preco_unitario
            print(f"Produto: {produto.nome}, Último Valor Unitário: {valor_unitario}")
            valor_total_estoque = valor_total_estoque + (valor_unitario * produto.quantidade)
        else:
            sem_entrada_registrada = sem_entrada_registrada + 1
            print(f"Produto: {produto.nome}, Sem entradas registradas")
    produtos_total = produtosAtual.count()

    # Quantidade de produtos abaixo do estoque mínimo
    produtos_abaixo_minimo = Produto.objects.filter(quantidade__lt=F('estoque_minimo')).count()

    context = {
        'valor_total_estoque': valor_total_estoque,
        'sem_entrada_registrada': sem_entrada_registrada,
        'produtos_total': produtos_total,
        'produtos_abaixo_minimo': produtos_abaixo_minimo,
    }

    return render(request, 'dashboard.html', context)

@login_required    
def produtos_view(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoForm()
    
    produtos = Produto.objects.all().order_by("nome")
    #Filtra os produtos por nome, categoria e local
    nome = request.GET.get('nome')
    categoria = request.GET.get('categoria')
    local = request.GET.get('local')
        
    if nome:
        produtos = produtos.filter(nome__icontains=nome)
    if categoria:
        produtos = produtos.filter(categoria__categoriaNome__icontains=categoria)
    if local:
        produtos = produtos.filter(local__localNome__icontains=local)        
    
    return render(request, 'produtos.html', {'produtos': produtos, 'form': form })

@login_required
def add_product(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
           form.save()
           return redirect('product')
    else:
        form = ProdutoForm()
    return render(request, 'add_product.html', {'form': form})

@login_required
def entradas_view(request):
    entradas = Entrada.objects.all().order_by("produto__nome")

    # Filtra entradas
    produto = request.GET.get('produto')
    tipo = request.GET.get('tipo')
    fornecedor = request.GET.get('fornecedor')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    if produto:
        entradas = entradas.filter(Q(produto__nome__icontains=produto))
    if tipo:
        entradas = entradas.filter(Q(tipo__icontains=tipo))
    if fornecedor:
        entradas = entradas.filter(Q(fornecedor__nome__icontains=fornecedor))
    if data_inicial and data_final:
        entradas = entradas.filter(criado_em__range=[data_inicial, data_final])
    
    return render(request, 'entradas.html', {'entradas': entradas})

@login_required    
def add_entrada_view(request):
    if request.method == 'POST':
        form = EntradasForm(request.POST)
        if form.is_valid():          
            form.save()
            messages.success(request, 'Entrada salva com sucesso!')
            return redirect('entradas')
        else:
            form = EntradasForm()        
            # Redirecione para outra página ou retorne uma resposta de sucesso
            return redirect('product')
    else:
        produto_id = request.GET.get('produto_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': produto_id, 'usuario': user_id}
        form = EntradasForm(initial=initial_data)
    return render(request, 'add_entrada.html', {'form': form})  

@login_required    
def saidas_view(request):
    saidas = Saida.objects.all().order_by("produto__nome")
    # Filtra saidas 
    produto = request.GET.get('produto')
    setor = request.GET.get('setor')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()

    if produto:
        saidas = saidas.filter(Q(produto__nome__icontains=produto))
    if setor:
        saidas = saidas.filter(Q(setor__setorNome__icontains=setor))
    if data_inicial and data_final:
        saidas = saidas.filter(criado_em__range=[data_inicial, data_final])
    return render(request, 'saidas.html', {'saidas': saidas})

@login_required
def add_saida_view(request):
    if request.method == 'POST':
        form = SaidasForm(request.POST)
        if form.is_valid():
            quantidade = form.cleaned_data['quantidade']
            produto = form.cleaned_data['produto']
            
            if quantidade > produto.quantidade:
                # The entered quantity exceeds the available stock
                # Display an appropriate error message to the user
                form.add_error('quantidade', 'A quantidade informada excede o estoque disponível.')
            else:
                form.save()
                messages.success(request, 'Saída salva com sucesso!')
                return redirect('saidas')
        # If the form is invalid, render the form with errors
    else:
        produto_id = request.GET.get('produto_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': produto_id, 'usuario': user_id}
        form = SaidasForm(initial=initial_data)
    
    return render(request, 'add_saida.html', {'form': form})

@login_required    
def pedidos_view(request):
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido salvo com sucesso!')
            return redirect('pedidos')
    else:
        form = PedidoForm()
    
    pedidos = Pedido.objects.all().order_by("-criado_em")
    #Filtra os produtos por nome, categoria e local
    id = request.GET.get('id')
    fornecedor = request.GET.get('fornecedor')
    status = request.GET.get('status')
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    if data_inicial:
        data_inicial = datetime.strptime(data_inicial, '%Y-%m-%d').date()
    if data_final:
        data_final = datetime.strptime(data_final, '%Y-%m-%d').date()
    
    if id:
        pedidos = pedidos.filter(id__icontains=id)
    if fornecedor:
        pedidos = pedidos.filter(fornecedor__nome__icontains=fornecedor)
    if status:
        pedidos = pedidos.filter(status__icontains=status)        
        
    return render(request, 'pedidos.html', {'pedidos': pedidos, 'form': form})

@login_required
def add_produto_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)

    if request.method == 'POST':
        form = ProdutoPedidoForm(request.POST)
        if form.is_valid():
            produto_pedido = form.save(commit=False)
            produto_pedido.pedido = pedido
            produto_pedido.save()
            #messages.success(request, 'Produto adicionado ao pedido com sucesso!')
            return redirect('detalhes_pedido', pedido_id=pedido.id)
    else:
        form = ProdutoPedidoForm()

    todos_produtos = Produto.objects.all()  # Obtenha todos os produtos disponíveis

    return render(request, 'detalhes_pedido.html', {'form': form, 'pedido': pedido, 'todos_produtos': todos_produtos})

@login_required
def editar_produto_view(request, produto_id):
    produto = get_object_or_404(Produto, id=produto_id)
    
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            return redirect('produtos')
    else:
        form = ProdutoForm(instance=produto)
    
    return render(request, 'editar_produto.html', {'form': form, 'produto': produto})


@login_required
def detalhes_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    produtos_pedidos = ProdutoPedido.objects.filter(pedido=pedido)

    if request.method == 'POST':
        form = ProdutoPedidoForm(request.POST)
        if form.is_valid():
            produto_pedido = form.save(commit=False)
            produto_pedido.pedido = pedido
            produto_pedido.save()
            # messages.success(request, 'Produto adicionado ao pedido com sucesso!')
            return redirect('detalhes_pedido', pedido_id=pedido.id)
    else:
        form = ProdutoPedidoForm()

    todos_produtos = Produto.objects.all()  # Obtenha todos os produtos disponíveis

    return render(request, 'detalhes_pedido.html', {'form': form, 'pedido': pedido, 'produtos_pedidos': produtos_pedidos, 'todos_produtos': todos_produtos})


@login_required
def remover_produto_pedido_view(request, pedido_id, produto_pedido_id):
    # Recupera o produto do pedido
    produto_pedido = get_object_or_404(ProdutoPedido, id=produto_pedido_id)

    # Verifica se o produto pertence ao pedido fornecido
    if produto_pedido.pedido_id != pedido_id:
        return redirect('detalhes_pedido', pedido_id=pedido_id)

    # Remove o produto do pedido
    produto_pedido.delete()

    return redirect('detalhes_pedido', pedido_id=pedido_id)

@login_required
def editar_pedido_view(request, pedido_id):
    pedido = get_object_or_404(Pedido, id=pedido_id)
    
    if request.method == 'POST':
        form = PedidoForm(request.POST, instance=pedido)
        if form.is_valid():
            form.save()
            return redirect('pedidos')
    else:
        form = PedidoForm(instance=pedido)
    
    return render(request, 'editar_pedido.html', {'form': form, 'pedido': pedido})

@login_required
def fornecedores_view(request):
    fornecedores = Fornecedor.objects.all()
    #Filtros
    nome = request.GET.get('nome')
    fone = request.GET.get('fone')
    email = request.GET.get('email')
  
    if nome:
        fornecedores = fornecedores.filter(nome__icontains=nome)
    if fone:
        fornecedores = fornecedores.filter(fone__icontains=fone)
    if email:
        fornecedores = fornecedores.filter(email__icontains=email)  
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('fornecedores')
    else:
        form = FornecedorForm()
    
    return render(request, 'fornecedores.html', {'fornecedores': fornecedores, 'form': form})

@login_required
def editar_fornecedor_view(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)

    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor salvo com sucesso!')
            return redirect('fornecedores')
    else:
        form = FornecedorForm(instance=fornecedor)

    return render(request, 'editar_fornecedor.html', {'form': form, 'fornecedor': fornecedor})

@login_required
def remover_fornecedor_view(request, fornecedor_id):
    fornecedor = get_object_or_404(Fornecedor, id=fornecedor_id)
    
    if request.method == 'POST':
        fornecedor.delete()
        return redirect('fornecedores')
    
    return redirect('fornecedores')


# Create your views here.
