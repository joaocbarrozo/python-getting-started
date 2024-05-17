from django import forms
from .models import Compra, Fornecedor, ItemNF, Produto, Pedido, ProdutoPedido, Entrada, Saida
from django.db.models import Q

class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'descricao', 'categoria', 'local','quantidade', 'estoque_minimo']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control', 'autocapitalize': 'characters'}),
            'descricao': forms.TextInput(attrs={'class': 'form-control', 'autocapitalize': 'characters'}),
            'categoria': forms.Select(attrs={'class': 'form-control'}),
            'local': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'estoque_minimo': forms.NumberInput(attrs={'class': 'form-control'}),
        }


class EntradasForm(forms.ModelForm):
    class Meta:
        model = Entrada
        fields = ['produto', 'tipo', 'item_nfe_id']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'item_nfe_id' : forms.Select(attrs={'class': 'form-control'})
            #'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            #'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            #'preco_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            #'usuario': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        queryset = self.fields['item_nfe_id'].queryset

        # Filter by items with status = "N"
        filter_condition = Q(status="N")
        ordering = ['descricao']  # Order by the 'descricao' field (replace with your desired field)

        # Apply the filter to the queryset (if present or create a new one)
        if queryset is not None:
            self.fields['item_nfe_id'].queryset = queryset.filter(filter_condition).order_by(*ordering)
        else:
            self.fields['item_nfe_id'].queryset = ItemNF.objects.filter(filter_condition).order_by(*ordering)
        
class SaidasForm(forms.ModelForm):
    class Meta:
        model = Saida
        fields = ['produto', 'setor', 'quantidade']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'setor': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            #'usuario': forms.Select(attrs={'class': 'form-control'}),
        }
        
        def clean_quantidade(self):
            quantidade = self.cleaned_data.get('quantidade')
            produto = self.cleaned_data.get('produto')

            if quantidade and produto:
                if quantidade > produto.quantidade:
                    raise forms.ValidationError('Quantidade indisponível em estoque.')

            return quantidade

class PedidoForm(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ["fornecedor", "status"]
        widgets = {
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
        }

class ProdutoPedidoForm(forms.ModelForm):
    class Meta:
        model = ProdutoPedido
        fields = ["produto", "quantidade"]
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
        }
    
class FornecedorForm(forms.ModelForm):
    class Meta:
        model = Fornecedor
        fields = ['cnpj','razao_social','nome', 'fone', 'email', 'contato',
                  'estado', 'municipio', 'bairro', 'endereco', 'numero', 'cep']
        widgets = {
            'cnpj': forms.TextInput(attrs={'class': 'form-control'}),
            'razao_social': forms.TextInput(attrs={'class': 'form-control'}),
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'fone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'estado': forms.TextInput(attrs={'class': 'form-control'}),
            'municipio': forms.TextInput(attrs={'class': 'form-control'}),
            'bairro': forms.TextInput(attrs={'class': 'form-control'}),
            'endereco': forms.TextInput(attrs={'class': 'form-control'}),
            'numero': forms.TextInput(attrs={'class': 'form-control'}),
            'cep': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
class FiltroDataForm(forms.Form):
    data_inicial = forms.DateField(label='Data Inicial', widget=forms.DateInput(attrs={'type': 'date'}))
    data_final = forms.DateField(label='Data Final', widget=forms.DateInput(attrs={'type': 'date'}))

from django import forms

class UploadXMLForm(forms.Form):
    xml_file = forms.FileField(widget=forms.ClearableFileInput(attrs={'onchange': 'updateFileName(this)'}))

class CompraForm(forms.ModelForm):
    class Meta:
        model = Compra
        fields = ['numero_id', 'numero', 'data_emissao', 'fornecedor', 'status']
        widgets = {
            'numero_id': forms.TextInput(attrs={'class': 'form-control'}),
            'numero' : forms.TextInput(attrs={'class': 'form-control'}),
            'data_emissao': forms.TextInput(attrs={'class': 'form-control'}),
            'fornecedor' : forms.TextInput(attrs={'class': 'form-control'}),
            
            'status' : forms.TextInput(attrs={'class': 'form-control'})
        }
