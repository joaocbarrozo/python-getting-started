from django import forms
from .models import Fornecedor, Produto, Pedido, ProdutoPedido, Entrada, Saida

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
        fields = ['produto', 'tipo', 'fornecedor', 'quantidade', 'preco_unitario']
        widgets = {
            'produto': forms.Select(attrs={'class': 'form-control'}),
            'tipo': forms.Select(attrs={'class': 'form-control'}),
            'fornecedor': forms.Select(attrs={'class': 'form-control'}),
            'quantidade': forms.NumberInput(attrs={'class': 'form-control'}),
            'preco_unitario': forms.NumberInput(attrs={'class': 'form-control'}),
            #'usuario': forms.Select(attrs={'class': 'form-control'}),
        }
        
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
        fields = ['nome', 'fone', 'email']
        widgets = {
            'nome': forms.TextInput(attrs={'class': 'form-control'}),
            'fone': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
        }
    
class FiltroDataForm(forms.Form):
    data_inicial = forms.DateField(label='Data Inicial', widget=forms.DateInput(attrs={'type': 'date'}))
    data_final = forms.DateField(label='Data Final', widget=forms.DateInput(attrs={'type': 'date'}))
