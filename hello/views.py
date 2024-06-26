from urllib import request
from django.shortcuts import get_object_or_404, render, redirect
from .models import Compra, Fornecedor, ItemNF, Produto, Pedido, ProdutoPedido, Entrada, Saida
from django.contrib.auth import logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .forms import CompraForm, FiltroDataForm, FornecedorForm, ProdutoForm, PedidoForm, ProdutoPedidoForm, EntradasForm, SaidasForm, UploadXMLForm
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
            messages.error(request, 'Nome de usuário ou senha inválidos. Tente novamente.')
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
    produtos = Produto.objects.all().order_by("nome")   
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto salvo com sucesso!')
            return redirect('produtos')
    else:
        form = ProdutoForm()  
    
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
    if request.method == 'POST':
        form = UploadXMLForm(request.POST, request.FILES)
        if form.is_valid():
            xml_file = request.FILES['xml_file']
            print('Arquivo recebido!')
            # Processar o arquivo XML e salvar os dados no banco de dados
            processar_xml(xml_file)
            return redirect('produtos')
        print(form.is_valid())
    else:
        form = UploadXMLForm()
        
    return render(request, 'entradas.html', {'entradas': entradas, 'form':form})


@login_required    
def add_entrada_view(request):
    if request.method == 'POST':
        form = EntradasForm(request.POST)
        if form.is_valid():          
            form.save()
            messages.success(request, 'Entrada salva com sucesso!')
            return redirect('itens_importados')
        else:
            form = EntradasForm()        
            # Redirecione para outra página ou retorne uma resposta de sucesso
            return redirect('itens_importados')
    else:
        produto_id = request.GET.get('produto_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': produto_id, 'usuario': user_id}
        form = EntradasForm(initial=initial_data)
    return render(request, 'add_entrada.html', {'form': form})  

@login_required
def compras_view(request):#Exibe notas fiscais importadas e ou cadastradas
    compras = Compra.objects.all().order_by("data_emissao")
    if request.method == 'POST':
        form = CompraForm(request.POST)
        if form.is_valid():
            xml_file = request.FILES['xml_file']
            print('Arquivo recebido!')
            # Processar o arquivo XML e salvar os dados no banco de dados
            processar_xml(xml_file)
            return redirect('produtos')
        print(form.is_valid())
    else:
        form = CompraForm()
        
    return render(request, 'compras.html', {'compras': compras, 'form':form})

@login_required
def detalhes_compra_view(request, compra_id):
    compra = get_object_or_404(Compra, id=compra_id)
    itens_nfe = ItemNF.objects.filter(nfe_id=compra_id)

    return render(request, 'detalhes_compra.html', {'compra': compra, 'itens_nfe': itens_nfe})


@login_required
def itensImportados_view(request):
    itens = ItemNF.objects.filter(status="N").order_by("data_importacao")
    if request.method == 'POST':
        formXML = UploadXMLForm(request.POST, request.FILES)
        if formXML.is_valid():
            xml_file = request.FILES['xml_file']
            print('Arquivo recebido!')
            # Processar o arquivo XML e salvar os dados no banco de dados
            msg = processar_xml(xml_file)
            messages.info(request, msg)
        print(formXML.is_valid())
    else:
        formXML = UploadXMLForm()
    formEntrada = EntradasForm()
    formProduto = ProdutoForm()

    context = {
        'itens': itens, 'formXML': formXML, 'formEntradas': formEntrada, 'formProduto': formProduto
    }
    
    return render(request, 'itensImportados.html', context)

def processar_xml(xml_file):
    # Analisar o arquivo XML e extrair os dados
    # Aqui você usaria uma biblioteca como xml.etree.ElementTree ou lxml
    # Exemplo simplificado usando xml.etree.ElementTree:
    print("Processando arquivo ...")
    import xml.etree.ElementTree as ET
    # Verificar se o arquivo XML está vazio
    if not xml_file:
        print("O arquivo XML está vazio.")
        return

    # Ler o conteúdo do arquivo XML
    xml_content = xml_file.read().decode('utf-8')

    # Analisar o conteúdo XML
    try:
        tree = ET.fromstring(xml_content)
        nf_e = {}
        
        # Encontrar o elemento infNFe 
        infNFe = tree.find('.//{http://www.portalfiscal.inf.br/nfe}infNFe')

        # Extrair o valor do atributo Id
        if infNFe is not None:
            nfe_id = infNFe.attrib.get('Id')
            nf_e = nfe_id[3:]#Retirando os 3 primeiros caracteres (NFe)
            print("ID da NF-e:", nf_e)
        else:
            print("Elemento infNFe não encontrado.")
        #Se a NF-e não existir no banco de dados seguir com o processo de extração dos dados    
        nf_exists = Compra.objects.filter(numero_id=nf_e).exists()
        print("Wxiste NF-e? " + str(nf_exists))
        #Verifica se a NF-e já foi importada
        if not nf_exists:
            # Encontrar o elemento CNPJ
            cnpj_xml = tree.find(".//{http://www.portalfiscal.inf.br/nfe}CNPJ").text
            print("CNPJ: " + cnpj_xml)
            #Verificar se o cnpj já está cadastrado no banco de dados
            cnpj_exists = Fornecedor.objects.filter(cnpj=cnpj_xml).exists()
            print("Existe CNPJ? " + str(cnpj_exists))
            #Verifica se o fornecedor já está cadastrado
            if not cnpj_exists:
                #Coletar os dados do fornecedor e armazenar em um dicionario ou objeto
                fornecedor_data = {}
                fornecedor_data['cnpj'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}CNPJ').text
                fornecedor_data['fone'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}fone').text
                fornecedor_data['xNome'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}xNome').text
                fornecedor_data['xFant'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}xFant').text
                fornecedor_data['xLgr'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}xLgr').text
                fornecedor_data['nro'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}nro').text
                fornecedor_data['xBairro'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}xBairro').text
                fornecedor_data['xMun'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}xMun').text
                fornecedor_data['UF'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}UF').text
                fornecedor_data['CEP'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}CEP').text
                print(fornecedor_data)
                #Salvar os dados do fornecedor no banco de dados
                dados_fornecedor = Fornecedor.objects.create(
                cnpj = fornecedor_data['cnpj'],
                razao_social = fornecedor_data['xNome'],
                nome = fornecedor_data['xFant'], 
                fone = fornecedor_data['fone'],
                email = "",          
                contato = "",
                estado = fornecedor_data['UF'],
                municipio = fornecedor_data['xMun'],
                bairro = fornecedor_data['xBairro'],
                endereco = fornecedor_data['xLgr'], 
                numero = fornecedor_data['nro'],
                cep = fornecedor_data['CEP']
                )
                dados_fornecedor.save()
                #messages.success(request, "Dados do fornecedor salvo com sucesso!")
            else:
                print("Fornecedor já cadastrado")    
            #Coletar dados da NF e salvar no banco de dados
            NFe_data = {}
            NFe_data['IdNFe'] = nf_e
            NFe_data['nNF'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}nNF').text
            NFe_data['dhEmi'] = tree.find('.//{http://www.portalfiscal.inf.br/nfe}dhEmi').text
            print(NFe_data)
            #Salvar os dados da NF-e em Compra no banco de dados
            dados_nfe = Compra.objects.create(
            numero_id = NFe_data['IdNFe'],
            numero = NFe_data['nNF'],
            data_emissao = NFe_data['dhEmi'],
            fornecedor = Fornecedor.objects.get(cnpj=cnpj_xml),
            recebida_em = "", 
            status = 'E'
            )
            dados_nfe.save()
            contagem_itens = 0  
            # Iterar sobre cada elemento 'det' para extrair as informações dos itens
            for det in tree.findall('.//{http://www.portalfiscal.inf.br/nfe}det'):
                # Extrair as informações de cada item
                contagem_itens += 1
                item = {
                "cProd" : det.find('.//{http://www.portalfiscal.inf.br/nfe}cProd').text,
                "xProd" : det.find('.//{http://www.portalfiscal.inf.br/nfe}xProd').text,
                "uCom" : det.find('.//{http://www.portalfiscal.inf.br/nfe}uCom').text,
                "qCom" : "{:.2f}".format(float(det.find('.//{http://www.portalfiscal.inf.br/nfe}qCom').text)),
                "vUnCom" : "{:.2f}".format(float(det.find('.//{http://www.portalfiscal.inf.br/nfe}vUnCom').text)),
                "vProd" : "{:.2f}".format(float(det.find('.//{http://www.portalfiscal.inf.br/nfe}vProd').text))
                }
                print(item)
                print("---------------")
                dados_item = ItemNF.objects.create(
                    nfe_id = Compra.objects.get(numero_id=nf_e),
                    codigo = item["cProd"],
                    descricao = item["xProd"],
                    unidade = item["uCom"],
                    quantidade = item["qCom"],
                    preco_unitario = item['vUnCom'],
                    valor_total = item['vProd'],
                    status = "N"
                )
                #Salvando item no banco de dados
                dados_item.save()
                print("Produto:", item)
                print("--------------------")
            print(contagem_itens)
            return  str(contagem_itens) + " itens importados"
        else:
            return "NF-e já importada"
            #messages.warning(request,"NF-e já importada!")
    except ET.ParseError as e:
        print("Erro ao analisar o XML:", e)
    
@login_required    
def saidas_view(request):
    saidas = Saida.objects.all().order_by("produto__nome")

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
                return redirect('produtos')
        # If the form is invalid, render the form with errors
    else:
        produto_id = request.GET.get('produto_id')
        user_id = request.GET.get('user_id')
        initial_data = {'produto': produto_id, 'usuario': user_id}
        form = SaidasForm(initial=initial_data)
    
    return render(request, 'add_saida.html', {'form': form})

@login_required    
def pedidos_view(request):
    pedidos = Pedido.objects.all().order_by("-criado_em") 
    if request.method == 'POST':
        form = PedidoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Pedido salvo com sucesso!')
            return redirect('pedidos')
    else:
        form = PedidoForm()
     
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
    produtos_pedidos = ProdutoPedido.objects.filter(pedido=pedido).order_by('produto__nome')

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
