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
                      },
                      text: 'Condicionais',
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
      buttons: [{ extend: 'copy', text: 'Copiar'}, 'csv', 'excel', 'pdf', 'print'],
      lengthChange: true,
      responsive: true,
      colReorder: true, // Ativar reordenação de colunas
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
            "buttons": {
                "copyTitle": 'Cópia de Tabela', // Defina o título da janela de diálogo de cópia
                "copySuccess": {
                    "_": '%d linhas copiadas',
                    "1": '1 linha copiada' // Defina a mensagem para exibir quando uma linha é copiada
                }
            },
            searchBuilder: {
                add: 'Adicionar Condição',
                button: {
                    0: 'Condicionais',
                    1: 'Condição (1)',
                    _: 'Condições (%d)'
                },
                clearAll: 'Limpar Tudo',
                condition: 'Condição',
                conditions: 'Condições',
                data: 'Dado',
                delete: 'Excluir',
                deleteTitle: 'Excluir Condição',
                left: 'Esquerda',
                leftTitle: 'Esquerda',
                logicAnd: 'E',
                logicOr: 'Ou',
                right: 'Direita',
                rightTitle: 'Direita',
                title: 'Construtor de Pesquisa',
                value: 'Valor',
                valueJoiner: 'União de Valor',
                conditions: {
                    date: {
                        after: 'Depois de',
                        before: 'Antes de',
                        between: 'Entre',
                        empty: 'Vazia',
                        equals: 'Igual a',
                        not: 'Diferente de',
                        notBetween: 'Não entre',
                        notEmpty: 'Não vazia'
                    },
                    array: {
                        contains: 'Contem',
                        empty: 'vazio',
                        equals: 'Igual a',
                        not: 'Diferente de',
                        notEmpty: 'Não vazio',
                        without: 'Sem'
                    },
                    string: {
                        contains: 'Contem',
                        empty: 'Vazio',
                        endsWith: 'Termina com',
                        equals: 'Igual a',
                        not: 'Diferente de',
                        notContains: 'Não Contem',
                        notEmpty: 'Não vazio',
                        notEndsWith: 'Não termina com',
                        notStartsWith: 'Não começa com',
                        startsWith: 'Começa com'
                    },
                    number: {
                        between: 'Entre',
                        empty: 'Vazio',
                        equals: 'Igual a',
                        gt: 'Maior que',
                        gte: 'Maior ou igual a',
                        lt: 'Menor que',
                        lte: 'Menor ou igual a',
                        not: 'Diferente de',
                        notBetween: 'Não entre',
                        notEmpty: 'Não vazio'
                    }
                }
            }, 
            searchPanes: {
                title: {
                    _: '%d Filtros Selecionados',
                    0: 'Nenhum Filtro Selecionado',
                    1: '1 Filtro Selecionado'
                },
                clearMessage: 'Limpar',
                collapse: 'Filtros',
                collapseMessage: 'Ocultar Filtros',
                count: '{total} registros',
                countFiltered: '{shown} ({total})',
                emptyMessage: 'Nenhum resultado',
                emptyPanes: 'Sem filtros aplicados',
                loadMessage: 'Carregando filtros...',
                showMessage: 'Mostrar filtros',
            }
        }
    });
  });
  