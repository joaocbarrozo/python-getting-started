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


  $(document).ready(function() {
    $('.table').DataTable({
      layout: {
          top: 'buttons',
          topStart: {
              buttons: [
                  {
                      extend: 'searchBuilder',
                      config: {
                          depthLimit: 2,
                          conditions: {
                              'date': {
                                  '==': 'Igual a',
                                  '!=': 'Diferente de',
                                  '<': 'Menor que',
                                  '<=': 'Menor ou igual a',
                                  '>': 'Maior que',
                                  '>=': 'Maior ou igual a',
                                  'between': 'Entre',
                                  'notBetween': 'Não entre',
                                  'empty': 'Vazio',
                                  'notEmpty': 'Não vazio'
                              }
                          }
                      },
                      text: 'Condicionais'
                  },
                  {
                      extend: 'searchPanes',
                      config: {
                          cascadePanes: true,
                          layout: 'columns-4'
                      },
                      text: 'Filtros'
                  },
                  {
                      extend: 'colvis',
                      text: 'Colunas'
                  }
              ],
          }
      },
      buttons: true,
      lengthChange: true,
      responsive: true,
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
    });
  });
  