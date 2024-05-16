//Função para esconder e exibir filtro
function esconderFiltro() {
    var formFiltro = document.getElementById("formFiltro");
    if (formFiltro.style.display === "none") {
      formFiltro.style.display = "block";
    } else {
      formFiltro.style.display = "none";
    }
  }

// Função para imprimir 
function imprimir() {
     window.print(); // Aciona a função de impressão do navegador
  }

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
          "oAria": {
              "sSortAscending": ": Ordenar colunas de forma ascendente",
              "sSortDescending": ": Ordenar colunas de forma descendente"
          },
          "select": {
              "rows": {
                  "_": "Selecionado %d linhas",
                  "0": "Nenhuma linha selecionada",
                  "1": "Selecionado 1 linha"
              }
          }
      },
      "colReorder": true, // Ativar reordenação de colunas
     
      "colVis": {
          "buttonText": 'Selecionar colunas',
          "overlayFade": 0,
          "exclude": [0] // Colunas que não podem ser escondidas
      }
  });
});


