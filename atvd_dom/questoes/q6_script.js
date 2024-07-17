document.addEventListener("DOMContentLoaded", function() {
    var botao = document.getElementById("mudarCor");

    botao.addEventListener("click", function() {
        var paragrafo = document.getElementById("paragrafo");
        paragrafo.style.color = "blue";
    });
});
