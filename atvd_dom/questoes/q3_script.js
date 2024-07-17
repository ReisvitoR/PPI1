document.addEventListener("DOMContentLoaded", function() {
    const divConteudo = document.getElementById('conteudo');
    const divResultado = document.getElementById('resultado');
    const botaoContar = document.getElementById('contar');

    botaoContar.addEventListener('click', function() {
        const paragrafos = divConteudo.getElementsByTagName('p');
        const numeroDeParagrafos = paragrafos.length;

        divResultado.textContent = `Número de parágrafos: ${numeroDeParagrafos}`;
    });
});
