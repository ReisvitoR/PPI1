import os
import requests
from bs4 import BeautifulSoup
from datetime import datetime
import re

class Pagina:
    def __init__(self, url, conteudo, data_publicacao):
        self.url = url
        self.conteudo = conteudo
        self.data_publicacao = data_publicacao
        self.links_recebidos = []
        self.pontos_autoridade = 0
        self.pontos_termos = 0
        self.pontos_tags = 0
        self.pontos_penalizacao = 0
        self.pontos_frescor = 0

    def adicionar_link(self, pagina):
        self.links_recebidos.append(pagina)

    def calcular_autoridade(self):
        self.pontos_autoridade = len(self.links_recebidos) * 20

    def calcular_termos(self, termos):
        for termo in termos:
            self.pontos_termos += self.conteudo.lower().count(termo.lower()) * 5

    def calcular_tags(self, termos_tags):
        soup = BeautifulSoup(self.conteudo, 'html.parser')
        for tag, peso in termos_tags.items():
            self.pontos_tags += len(soup.find_all(tag)) * peso

    def penalizar_autoreferencia(self):
        for link in self.links_recebidos:
            if link.url == self.url:
                self.pontos_penalizacao -= 20

    def calcular_frescor(self, ano_atual):
        anos_desde_publicacao = ano_atual - self.data_publicacao.year
        self.pontos_frescor = 30 - (anos_desde_publicacao * 5)

    def calcular_pontuacao_total(self):
        return (self.pontos_autoridade +
                self.pontos_termos +
                self.pontos_tags +
                self.pontos_penalizacao +
                self.pontos_frescor)

class Buscador:
    def __init__(self):
        self.paginas = {}
        self.paginas_visitadas = set()
        self.arquivo_links = 'links.txt'

    def adicionar_pagina(self, url, conteudo, data_publicacao):
        if url not in self.paginas:
            self.paginas[url] = Pagina(url, conteudo, data_publicacao)

    def adicionar_link(self, origem, destino):
        if origem in self.paginas and destino in self.paginas:
            self.paginas[destino].adicionar_link(self.paginas[origem])

    def indexar_pagina_web(self, url, termos, termos_tags):
        try:
            response = requests.get(url)
            termos = re.split(r',\s*', input("Digite os termos de busca separados por vírgula: "))
            if response.status_code == 200:
                self.indexar_pagina(url, response.text, termos, termos_tags)  # Correção aqui
            else:
                print(f"Erro ao baixar a página {url}. Status Code: {response.status_code}")
        except Exception as e:
            print(f"Erro ao baixar a página {url}: {e}")

    def indexar_paginas_locais(self, diretorio, termos, termos_tags):
        for dirpath, _, filenames in os.walk(diretorio):
            for filename in filenames:
                if filename.endswith('.html'):
                    filepath = os.path.join(dirpath, filename)
                    with open(filepath, 'r', encoding='utf-8') as file:
                        conteudo = file.read()
                        self.indexar_pagina(filepath, conteudo, termos, termos_tags)

    def indexar_pagina(self, url, conteudo, termos, termos_tags):
        if url.startswith('http'):
            self.indexar_pagina_web(url, termos, termos_tags)
        else:
            self.indexar_pagina_local(url, conteudo, termos, termos_tags)

    def buscar(self, termo, termos_tags):
        ano_atual = datetime.now().year
        resultados = []

        for pagina in self.paginas.values():
            pagina.calcular_autoridade()
            pagina.calcular_termos([termo])
            pagina.calcular_tags(termos_tags)
            pagina.penalizar_autoreferencia()
            pagina.calcular_frescor(ano_atual)

            pontuacao_total = pagina.calcular_pontuacao_total()

            if pontuacao_total > 0:
                resultados.append((pagina, pontuacao_total))

        # Ordenar por pontuação total, quantidade de termos, frescor e número de links
        resultados = sorted(resultados, key=lambda x: (
        x[1], x[0].pontos_termos, x[0].pontos_frescor, len(x[0].links_recebidos)), reverse=True)
        return resultados

    def indexar_pagina_local(self, url, conteudo, termos, termos_tags):
        if url in self.paginas_visitadas:
            print(f"A página {url} já foi visitada.")
            return

        data_publicacao = datetime.now()  # Supondo que não temos a informação real da data de publicação
        self.adicionar_pagina(url, conteudo, data_publicacao)
        soup = BeautifulSoup(conteudo, 'html.parser')
        links = soup.find_all('a', href=True)
        for link in links:
            link_url = link['href']
            self.adicionar_link(url, link_url)
        self.paginas_visitadas.add(url)

    def buscar_palavra_chave(self):
        termo = input("Digite a palavra-chave que deseja buscar: ")
        termos_tags = {"title": 20, "h1": 15, "h2": 10, "p": 5, "a": 2}
        resultados = self.buscar(termo, termos_tags)
        self.ultimos_resultados = resultados 
        self.exibir_resultados(resultados)

    def exibir_resultados(self, resultados):
        print("\nResultados da busca:")
        for i, (pagina, pontuacao) in enumerate(resultados):
            print(f"{i + 1}. {pagina.url}")
            print(f"   - Autoridade das Páginas: {pagina.pontos_autoridade}")
            print(f"   - Quantidade dos Termos Buscados: {pagina.pontos_termos}")
            print(f"   - Uso das Tags (head, h1, h2, p) para Relevância: {pagina.pontos_tags}")
            print(f"   - Penalização por Autoreferência: {pagina.pontos_penalizacao}")
            print(f"   - Frescor do Conteúdo: {pagina.pontos_frescor}")
            print(f"   - Pontuação Total: {pontuacao}")

    def mostrar_criterios(self):
        print("\nCritérios de Ranqueamento:")
        print("1. Autoridade das Páginas: Determinada pela quantidade de links recebidos de outras páginas. Cada link recebido vale +20 pontos.")
        print("2. Quantidade dos Termos Buscados: Frequência com que os termos buscados aparecem no código-fonte da página. Cada ocorrência do termo buscado vale +5 pontos.")
        print("3. Uso das Tags (head, h1, h2, p) para Relevância: Pontos atribuídos pelo uso de termos buscados em várias tags.")
        print("   - Title e Meta tags: +20 pontos cada")
        print("   - h1: +15 pontos cada ocorrência")
        print("   - h2: +10 pontos cada ocorrência")
        print("   - p: +5 pontos cada ocorrência")
        print("   - a: +2 pontos cada ocorrência")
        print("4. Penalização por Autoreferência: Cada autoreferência resulta em uma penalidade de -20 pontos.")
        print("5. Frescor do Conteúdo: Avaliado pela data de publicação da página.")
        print("   - Páginas publicadas no ano corrente recebem +30 pontos.")
        print("   - Redução de -5 pontos para cada ano anterior.")
        print("6. Pontuação Total: Soma dos pontos atribuídos pelos critérios acima.")

    def menu(self):
        while True:
            print("\nMenu:")
            print("1. Indexar página local")
            print("2. Indexar página web")
            print("3. Buscar palavra-chave")
            print("4. Exibir resultados da última busca")
            print("5. Mostrar critérios de ranqueamento")
            print("6. Sair")

            escolha = input("Escolha uma opção: ")
            if escolha == '1':
                diretorio = input("Digite o caminho do diretório contendo os arquivos HTML: ")
                termos = input("Digite os termos de busca separados por vírgula: ").split(',')
                termos = [termo.strip() for termo in termos]  # Remover espaços extras em cada termo
                termos_tags = {"title": 20, "h1": 15, "h2": 10, "p": 5, "a": 2}
                self.indexar_paginas_locais(diretorio, termos, termos_tags)
            elif escolha == '2':
                url = input("Digite a URL da página para indexar: ")
                termos = input("Digite os termos de busca separados por vírgula: ").split(',')
                termos = [termo.strip() for termo in termos]  # Remover espaços extras em cada termo
                termos_tags = {"title": 20, "h1": 15, "h2": 10, "p": 5, "a": 2}
                self.indexar_pagina_web(url, termos, termos_tags)
            elif escolha == '3':
                self.buscar_palavra_chave()
            elif escolha == '4':
                if hasattr(self, 'ultimos_resultados'):
                    self.exibir_resultados(self.ultimos_resultados)
                else:
                    print("Nenhum resultado disponível. Realize uma busca primeiro.")
            elif escolha == '5':
                self.mostrar_criterios()
            elif escolha == '6':
                print("Saindo...")
                break
            else:
                print("Opção inválida. Por favor, escolha uma opção válida.")

# Exemplo de uso:
buscador = Buscador()
buscador.menu()
