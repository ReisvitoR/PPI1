//POR ID
document.addEventListener("DOMContentLoaded", function() {
    const titulo = document.getElementById('titulo');
    const botao = document.getElementById('botao');

    botao.addEventListener('click', function() {
        titulo.textContent = 'Você clicou no botão!';
    });
});
