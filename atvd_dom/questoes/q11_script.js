document.addEventListener("DOMContentLoaded", function() {
    var botaoAdicionar = document.getElementById("adicionar");
    var caixaTexto = document.getElementById("caixaTexto");
    var lista = document.getElementById("lista");

    botaoAdicionar.addEventListener("click", function() {
        var texto = caixaTexto.value.trim(); // Obtém o texto da caixa

        if (texto) { // Verifica se a caixa não está vazia
            // Cria um novo item de lista
            var novoItem = document.createElement("li");
            novoItem.textContent = texto;

            // Adiciona o item à lista
            lista.appendChild(novoItem);

            // Limpa a caixa de texto
            caixaTexto.value = "";
        }
    });
});
