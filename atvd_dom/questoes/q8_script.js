document.addEventListener("DOMContentLoaded", function() {
    var botaoAltoContraste = document.getElementById("altoContraste");
    var botaoResetar = document.getElementById("resetar");

    botaoAltoContraste.addEventListener("click", function() {
        document.body.style.backgroundColor = "black";
        document.body.style.color = "white";
    });

    botaoResetar.addEventListener("click", function() {
        document.body.style.backgroundColor = "white";
        document.body.style.color = "black";
    });
});
