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
