import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin

class PaginaWeb:
    def __init__(self, url, data_publicacao):
        self.url = url
        self.links_recebidos = 0
        self.ocorrencias = {}
        self.tags = {
            'title': 0,
            'meta': 0,
            'h1': 0,
            'h2': 0,
            'p': 0,
            'a': 0
        }
        self.autoreferencias = set()
        self.data_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d")
        self.links = []

    def adicionar_link(self, origem):
        if origem == self.url:
            self.autoreferencias.add(origem)
        else:
            self.links_recebidos += 1

    def adicionar_ocorrencia(self, termo):
        if termo in self.ocorrencias:
            self.ocorrencias[termo] += 1
        else:
            self.ocorrencias[termo] = 1

    def adicionar_tag(self, tag):
        if tag in self.tags:
            self.tags[tag] += 1

    def calcular_pontuacao_autoridade(self):
        return self.links_recebidos * 20

    def calcular_pontuacao_termos(self, termos_buscados):
        pontuacao = 0
        for termo in termos_buscados:
            if termo in self.ocorrencias:
                pontuacao += self.ocorrencias[termo] * 5
        return pontuacao

    def calcular_pontuacao_tags(self, termos_buscados):
        pontuacao = 0
        for tag, quantidade in self.tags.items():
            if tag == 'title' or tag == 'meta':
                pontuacao += quantidade * 20
            elif tag == 'h1':
                pontuacao += quantidade * 15
            elif tag == 'h2':
                pontuacao += quantidade * 10
            elif tag == 'p':
                pontuacao += quantidade * 5
            elif tag == 'a':
                pontuacao += quantidade * 2
        return pontuacao

    def aplicar_penalidade_autoreferencia(self):
        penalidade = len(self.autoreferencias) * -20
        return penalidade

    def calcular_pontuacao_frescor(self):
        ano_corrente = datetime.now().year
        anos_passados = ano_corrente - self.data_publicacao.year
        pontuacao = 30 - (anos_passados * 5)
        return pontuacao if pontuacao > 0 else 0

    def extrair_links(self, conteudo_pagina):
        soup = BeautifulSoup(conteudo_pagina, "html.parser")
        for link in soup.find_all('a', href=True):
            href = link['href']
            if href.startswith("http"):
                self.links.append(href)
            else:
                self.links.append(urljoin(self.url, href))


class Buscador:
    def __init__(self):
        self.paginas = []
        self.paginas_visitadas = set()  # Armazena os URLs das páginas já visitadas

    def baixar_pagina(self, url):
        try:
            resposta = requests.get(url, timeout=5)  # Definindo um timeout de 5 segundos
            # Verifica se a solicitação foi bem-sucedida (código de status 200)
            if resposta.status_code == 200:
                return resposta.text  # Retorna o conteúdo da página
            else:
                print(f"Falha ao baixar a página {url}. Código de status: {resposta.status_code}")
                return None
        except Exception as e:
            print(f"Erro ao baixar a página {url}: {str(e)}")
            return None

    def indexar_pagina(self, url, conteudo, data_publicacao):
        if url in self.paginas_visitadas:  # Verifica se a página já foi visitada
            print(f"A página {url} já foi visitada ✔.")
            return
        pagina = PaginaWeb(url, data_publicacao)
        pagina.extrair_links(conteudo)  # Extrai e armazena os links da página
        self.paginas.append(pagina)
        self.paginas_visitadas.add(url)  # Adiciona o URL da página à lista de páginas visitadas

    def buscar_e_indexar(self, url, data_publicacao):
        with open(url, 'r', encoding='utf-8') as file:
            content = file.read()
            soup = BeautifulSoup(content, "html.parser")
            for link in soup.find_all('a', href=True):
                href = link['href']
                if href.startswith("http"):
                    self.indexar_pagina(href, content, data_publicacao)
                else:
                    self.indexar_pagina(urljoin("file:", url, href), content, data_publicacao)

    def comparar_paginas(self, pagina1, pagina2, termos_buscados):
        # Critério a: Maior quantidade de termos buscados no corpo do texto
        pontuacao_termos_pagina1 = pagina1.calcular_pontuacao_termos(termos_buscados)
        pontuacao_termos_pagina2 = pagina2.calcular_pontuacao_termos(termos_buscados)
        if pontuacao_termos_pagina1 != pontuacao_termos_pagina2:
            return pontuacao_termos_pagina2 - pontuacao_termos_pagina1  # Ordenação decrescente

        # Critério b: Maior frescor do conteúdo
        pontuacao_frescor_pagina1 = pagina1.calcular_pontuacao_frescor()
        pontuacao_frescor_pagina2 = pagina2.calcular_pontuacao_frescor()
        if pontuacao_frescor_pagina1 != pontuacao_frescor_pagina2:
            return pontuacao_frescor_pagina2 - pontuacao_frescor_pagina1  # Ordenação decrescente

        # Critério c: Maior número de links recebidos
        if pagina1.links_recebidos != pagina2.links_recebidos:
            return pagina2.links_recebidos - pagina1.links_recebidos  # Ordenação decrescente

        # Se todos os critérios forem iguais, desempatar pela ordem alfabética do URL
        return 1 if pagina1.url > pagina2.url else -1 if pagina1.url < pagina2.url else 0

    def buscar_e_classificar(self, termos_buscados):
        # Classificar as páginas com base nos critérios de ranqueamento
        self.paginas.sort(key=lambda pagina: (pagina.calcular_pontuacao_termos(termos_buscados),
                                               pagina.calcular_pontuacao_frescor(),
                                               pagina.links_recebidos),                          reverse=True)

    def salvar_links(self, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:  # Modificado para 'w' (write)
            for pagina in self.paginas:
                arquivo.write(f"URL: {pagina.url}\n")
                arquivo.write("Links na página:\n")
                for link in pagina.links:
                    arquivo.write(f"{link}\n")
                arquivo.write("\n")  # Adiciona uma linha em branco entre as páginas

    def carregar_paginas_visitadas(self, nome_arquivo):
        try:
            with open(nome_arquivo, 'r') as arquivo:
                for linha in arquivo:
                    url = linha.strip()  # Remove espaços em branco e quebras de linha
                    self.paginas_visitadas.add(url)
        except FileNotFoundError:
            print("Arquivo de páginas visitadas não encontrado. Criando um novo.")

    def salvar_paginas_visitadas(self, nome_arquivo):
        with open(nome_arquivo, 'w') as arquivo:  # Modificado para 'w' (write)
            for url in self.paginas_visitadas:
                arquivo.write(f"{url}\n")


def exibir_menu():
    print("== MENU ==")
    print("1. Inserir URL desejado")
    print("2. Mostrar pontuação geral")
    print("3. Sair")


def inserir_url(buscador):
    url = input("Digite o nome do arquivo HTML: ")
    data_publicacao = input("Digite a data de publicação (no formato YYYY-MM-DD): ")
    buscador.buscar_e_indexar(url, data_publicacao)


def mostrar_pontuacao_geral(buscador):
    termos_buscados = ["python", "javascript", "html"]
    buscador.buscar_e_classificar(termos_buscados)
    print("== PONTUAÇÃO GERAL ==")
    for i, pagina in enumerate(buscador.paginas, start=1):
        print(f"{i}. URL: {pagina.url} - Pontuação: {pagina.calcular_pontuacao_termos(termos_buscados)}")

with open("conf.json", "r") as config_file:
    config = json.load(config_file)

# Exemplo de uso:
buscador = Buscador()
buscador.carregar_paginas_visitadas("paginas_visitadas.txt")

while True:
    exibir_menu()
    escolha = input("Escolha uma opção: ")
    if escolha == '1':
        inserir_url(buscador)
    elif escolha == '2':
        mostrar_pontuacao_geral(buscador)
    elif escolha == '3':
        buscador.salvar_paginas_visitadas("paginas_visitadas.txt")
        print("Saindo do programa... Volte sempre *-*")
        break
    else:
        print("Opção inválida. Por favor, escolha uma opção válida.")

