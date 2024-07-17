document.addEventListener("DOMContentLoaded", function() {
    var botao = document.getElementById("copiar");
    
    botao.addEventListener("click", function() {
        var caixaTexto = document.getElementById("caixaTexto");
        var caixaTextoCaps = document.getElementById("caixaTextoCaps");
        
        // Copia o texto em capslock
        caixaTextoCaps.value = caixaTexto.value.toUpperCase();
    });
});
