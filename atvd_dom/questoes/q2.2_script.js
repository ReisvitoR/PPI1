//POR TAG NAME
document.addEventListener("DOMContentLoaded", function() {
    const titulo = document.getElementById('titulo');
    const botao = document.getElementById('botao');
    const paragrafos = document.getElementsByTagName('p');

    botao.addEventListener('click', function() {
        titulo.textContent = 'Você clicou no botão!';
        
        for (let i = 0; i < paragrafos.length; i++) {
            paragrafos[i].textContent = `Parágrafo ${i + 1} foi alterado!`;
        }
    });
});
