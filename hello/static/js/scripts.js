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