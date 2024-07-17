document.addEventListener("DOMContentLoaded", function() {
    var botaoAlterar = document.getElementById("alterar");
    var botaoLimpar = document.getElementById("limpar");

    botaoAlterar.addEventListener("click", function() {
        var paragrafo = document.getElementById("paragrafo");
        paragrafo.textContent = "O texto desse parágrafo foi alterado!";
    });

    botaoLimpar.addEventListener("click", function() {
        var paragrafo = document.getElementById("paragrafo");
        paragrafo.textContent = "";
    });
});
