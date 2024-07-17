document.addEventListener("DOMContentLoaded", function() {
    var botaoCalcular = document.getElementById("calcular");
    var resultado = document.getElementById("resultado");

    botaoCalcular.addEventListener("click", function() {
        var num1 = parseFloat(document.getElementById("num1").value);
        var num2 = parseFloat(document.getElementById("num2").value);
        var operacao;

        // Verifica qual operação foi selecionada
        var operacoes = document.getElementsByName("operacao");
        for (var i = 0; i < operacoes.length; i++) {
            if (operacoes[i].checked) {
                operacao = operacoes[i].value;
                break;
            }
        }

        var resultadoCalculo;

        // Realiza a operação com base na seleção
        switch (operacao) {
            case "adição":
                resultadoCalculo = num1 + num2;
                break;
            case "subtração":
                resultadoCalculo = num1 - num2;
                break;
            case "multiplicação":
                resultadoCalculo = num1 * num2;
                break;
            case "divisão":
                resultadoCalculo = num2 !== 0 ? num1 / num2 : "Erro: Divisão por zero!";
                break;
        }

        // Exibe o resultado
        resultado.textContent = "Resultado: " + resultadoCalculo;
    });
});
