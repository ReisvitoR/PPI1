import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from collections import defaultdict
from datetime import datetime

# Função para obter o conteúdo de uma página
def obter_conteudo_pagina(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.text
        else:
            return None
    except Exception as e:
        print("Erro ao obter conteúdo da página:", e)
        return None

# Função para extrair texto de uma página
def extrair_texto(html):
    soup = BeautifulSoup(html, 'html.parser')
    texto = soup.get_text()
    return texto

# Função para calcular a pontuação da página com base nos critérios
def calcular_pontuacao(url, termos_busca):
    pontuacao = 0
    conteudo = obter_conteudo_pagina(url)
    if conteudo:
        texto = extrair_texto(conteudo)
        for termo in termos_busca:
            pontuacao += texto.lower().count(termo.lower()) * 5
        soup = BeautifulSoup(conteudo, 'html.parser')
        pontuacao += len(soup.find_all(['title', 'meta'], string=termos_busca)) * 20
        pontuacao += len(soup.find_all('h1', string=termos_busca)) * 15
        pontuacao += len(soup.find_all('h2', string=termos_busca)) * 10
        pontuacao += len(soup.find_all('p', string=termos_busca)) * 5
        pontuacao += len(soup.find_all('a', string=termos_busca)) * 2
        
        if url in texto:
            pontuacao -= 20
            
        parsed_url = urlparse(url)
        try:
            year = datetime.now().year - int(parsed_url.netloc.split('.')[-1])
            frescor = max(0, year)
            pontuacao += frescor * -5
        except ValueError:
            print(f"A parte da URL '{parsed_url.netloc}' não pôde ser convertida em um número inteiro.")
        
    return pontuacao

# Função para normalizar a pontuação
def normalizar_pontuacao(pontuacoes):
    max_pontuacao = max(pontuacoes.values())
    min_pontuacao = min(pontuacoes.values())
    for url in pontuacoes:
        pontuacoes[url] = ((pontuacoes[url] - min_pontuacao) / (max_pontuacao - min_pontuacao)) * 100
    return pontuacoes

# Função principal do buscador
def buscar(termos_busca, urls):
    pontuacoes = defaultdict(int)
    for url in urls:
        pontuacoes[url] = calcular_pontuacao(url, termos_busca)
    pontuacoes_normalizadas = normalizar_pontuacao(pontuacoes)
    urls_ordenadas = sorted(pontuacoes_normalizadas, key=pontuacoes_normalizadas.get, reverse=True)
    return urls_ordenadas

# Função para receber os termos de busca do usuário
def receber_termos_busca():
    termos = input("Digite os termos de busca separados por vírgula: ")
    termos_busca = [termo.strip() for termo in termos.split(",")]
    return termos_busca

# Função para receber as URLs do usuário
def receber_urls():
    while True:
        num_urls = input("Quantas URLs deseja informar (máximo 5)? ")
        if num_urls.isdigit() and 0 < int(num_urls) <= 5:
            break
        else:
            print("Por favor, insira um número válido entre 1 e 5.")
    urls = []
    for i in range(int(num_urls)):
        url = input(f"Informe a URL {i+1}: ")
        urls.append(url.strip())
    return urls

# Exemplo de uso do buscador
if __name__ == "__main__":
    termos_busca = receber_termos_busca()
    if not termos_busca:
        print("Erro: Termos de busca não fornecidos.")
    else:
        urls = receber_urls()
        if not urls:
            print("Erro: Nenhuma URL fornecida.")
        else:
            resultados = buscar(termos_busca, urls)
            for i, url in enumerate(resultados, 1):
                print(f"{i}. {url}")
