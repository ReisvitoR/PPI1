document.addEventListener("DOMContentLoaded", function() {
    var botaoAdicionar = document.getElementById("adicionar");
    var caixaTexto = document.getElementById("caixaTexto");
    var selectLista = document.getElementById("selectLista");

    botaoAdicionar.addEventListener("click", function() {
        var texto = caixaTexto.value.trim(); // Obtém o texto da caixa

        if (texto) { // Verifica se a caixa não está vazia
            // Cria um novo elemento <option>
            var novoItem = document.createElement("option");
            novoItem.textContent = texto;
            novoItem.value = texto; // Define o valor do option

            // Adiciona o item ao select
            selectLista.appendChild(novoItem);

            // Limpa a caixa de texto
            caixaTexto.value = "";
        }
    });
});