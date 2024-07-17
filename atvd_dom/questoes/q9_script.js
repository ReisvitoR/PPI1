document.addEventListener("DOMContentLoaded", function() {
    var botaoAumentar = document.getElementById("aumentar");
    var botaoDiminuir = document.getElementById("diminuir");
    
    // Tamanho padrão do texto
    var tamanhoTexto = 16;

    botaoAumentar.addEventListener("click", function() {
        tamanhoTexto += 2; // Aumenta o tamanho do texto
        document.body.style.fontSize = tamanhoTexto + "px";
    });

    botaoDiminuir.addEventListener("click", function() {
        tamanhoTexto -= 2; // Diminui o tamanho do texto
        document.body.style.fontSize = tamanhoTexto + "px";
    });
});
