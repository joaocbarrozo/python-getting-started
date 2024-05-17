//Função para esconder e exibir filtro
function esconderFiltro() {
    var formFiltro = document.getElementById("formFiltro");
    if (formFiltro.style.display === "block") {
      formFiltro.style.display = "none";
    } else {
      formFiltro.style.display = "block";
    }
  }

// Função para imprimir 
function imprimir() {
     window.print(); // Aciona a função de impressão do navegador
  }

  //Script para remover a notificação após 5 segundos
  setTimeout(function() {
      document.querySelector('.alert').remove();
  }, 5000); // 5000 milissegundos = 5 segundos


//Função para exibir o nome do documento carregado na tela entradas
function updateFileName(input) {
    var fileNameElement = document.getElementById('fileName');
    if (input.files.length > 0) {
        fileNameElement.textContent = 'Arquivo selecionado: ' + input.files[0].name;
    } else {
        fileNameElement.textContent = '';
    }
}

//Função de tabela dinamica
$(document).ready(function() {
  $('.table').DataTable({
      "language": {
          "sEmptyTable": "Nenhum registro encontrado",
          "sInfo": "Mostrando de _START_ até _END_ de _TOTAL_ registros",
          "sInfoEmpty": "Mostrando 0 até 0 de 0 registros",
          "sInfoFiltered": "(Filtrados de _MAX_ registros)",
          "sInfoPostFix": "",
          "sInfoThousands": ".",
          "sLengthMenu": "Mostrar _MENU_ resultados por página",
          "sLoadingRecords": "Carregando...",
          "sProcessing": "Processando...",
          "sZeroRecords": "Nenhum registro encontrado",
          "sSearch": "Pesquisar",
          "oPaginate": {
              "sNext": "Próximo",
              "sPrevious": "Anterior",
              "sFirst": "Primeiro",
              "sLast": "Último"
          },
      },
      "colReorder": true, // Ativar reordenação de colunas
     
      "colVis": {
          "buttonText": 'Selecionar colunas',
          "overlayFade": 0,
          "exclude": [0] // Colunas que não podem ser escondidas
      }
  });
});


