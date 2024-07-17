import requests
from bs4 import BeautifulSoup
import re
from datetime import datetime

# Função para baixar o conteúdo de uma página e extrair os links
def baixar_conteudo_e_links(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            # Extrair os links da página
            soup = BeautifulSoup(response.text, 'html.parser')
            links = [link.get('href') for link in soup.find_all('a', href=True)]
            return True, response.text, links
        else:
            print(f"Erro ao baixar conteúdo da página: {response.status_code}")
            return False, None, []
    except Exception as e:
        print(f"Erro durante a solicitação HTTP: {str(e)}")
        return False, None, []

# Função para carregar as páginas visitadas a partir de um arquivo
def carregar_paginas_visitadas(arquivo_paginas_visitadas):
    try:
        with open(arquivo_paginas_visitadas, 'r') as file:
            return set([url.strip() for url in file.readlines()])
    except FileNotFoundError:
        return set()

# Função para salvar as páginas visitadas em um arquivo
def salvar_paginas_visitadas(paginas_visitadas, arquivo_paginas_visitadas):
    with open(arquivo_paginas_visitadas, 'w') as file:
        for url in paginas_visitadas:
            file.write(url + '\n')

# Função para baixar o conteúdo de uma página e extrair os links recursivamente
def baixar_conteudo_e_links_recursivo(url, max_profundidade, arquivo_paginas_visitadas, paginas_visitadas=set(), profundidade_atual=1):
    if profundidade_atual > max_profundidade or url in paginas_visitadas:
        return []

    sucesso, conteudo, links = baixar_conteudo_e_links(url)
    if sucesso:
        paginas_visitadas.add(url)  # Adiciona a URL às páginas visitadas
        salvar_paginas_visitadas(paginas_visitadas, arquivo_paginas_visitadas)  # Salva as páginas visitadas no arquivo
        links_recursivos = []
        for link in links:
            links_recursivos.extend(baixar_conteudo_e_links_recursivo(link, max_profundidade, arquivo_paginas_visitadas, paginas_visitadas, profundidade_atual + 1))
        return links + links_recursivos
    else:
        return []

# Função para calcular os pontos de autoridade das páginas
def calcular_pontos_autoridade(links):
    pontos = len(links) * 20
    print(f"Pontos de Autoridade: {pontos}")
    return pontos

# Função para calcular os pontos pela quantidade de termos buscados
def calcular_pontos_termos_buscados(texto, termos_buscados):
    pontos = 0
    for termo in termos_buscados:
        pontos += texto.count(termo) * 5
    print(f"Pontos pela Quantidade de Termos Buscados: {pontos}")
    return pontos

# Função para calcular os pontos pelo uso de tags para relevância
def calcular_pontos_tags_relevancia(html, termos_buscados):
    pontos = 0
    for termo in termos_buscados:
        pontos += len(re.findall(f'<title>|<meta.*?{termo}.*?>|<h1>{termo}|<h2>{termo}|<p>{termo}|<a.*?{termo}.*?>', html, re.IGNORECASE)) * 20
        pontos += html.count(f'<h1>{termo}') * 15
        pontos += html.count(f'<h2>{termo}') * 10
        pontos += html.count(f'<p>{termo}') * 5
        pontos += html.count(f'<a.*?{termo}.*?>') * 2
    print(f"Pontos pelo Uso de Tags para Relevância: {pontos}")
    return pontos

# Função para calcular os pontos pela frescor do conteúdo
def calcular_pontos_frescor(data_publicacao):
    ano_atual = datetime.now().year
    ano_publicacao = datetime.strptime(data_publicacao, "%Y-%m-%d").year
    pontos = max(30 - 5 * (ano_atual - ano_publicacao), 0)
    print(f"Pontos pelo Frescor do Conteúdo: {pontos}")
    return pontos

# Função para classificar as páginas
def classificar_paginas(paginas, termos_buscados):
    for pagina in paginas:
        pontos_autoridade = calcular_pontos_autoridade(pagina['links'])
        pontos_termos_buscados = calcular_pontos_termos_buscados(pagina['texto'], termos_buscados)
        pontos_tags_relevancia = calcular_pontos_tags_relevancia(pagina['html'], termos_buscados)
        pontos_frescor = calcular_pontos_frescor(pagina['data_publicacao'])
        penalidade_autoreferencia = -20 * pagina['autoreferencia']

        # Calcula a pontuação total
        pontuacao_total = pontos_autoridade + pontos_termos_buscados + pontos_tags_relevancia + pontos_frescor + penalidade_autoreferencia

        # Adiciona a pontuação total à página
        pagina['pontuacao'] = pontuacao_total
        print(f"Pontuação Total da Página: {pontuacao_total}")

    # Classifica as páginas em ordem decrescente de pontuação
    paginas_classificadas = sorted(paginas, key=lambda x: (x['pontuacao'], x['        # texto'].count(termos_buscados[0]), -calcular_pontos_frescor(x['data_publicacao']), len(x['links'])), reverse=True)
    return paginas_classificadas

# Exemplo de uso
if __name__ == "__main__":
    # URL da página inicial
    pagina_inicial_url = "https://exemplo.com"
    
    # Profundidade máxima para baixar páginas recursivamente
    max_profundidade = 2
    
    # Arquivo para armazenar as páginas visitadas
    arquivo_paginas_visitadas = "paginas_visitadas.txt"
    
    # Carregar as páginas visitadas do arquivo
    paginas_visitadas = carregar_paginas_visitadas(arquivo_paginas_visitadas)
    
    # Baixar o conteúdo da página inicial e extrair os links recursivamente
    links = baixar_conteudo_e_links_recursivo(pagina_inicial_url, max_profundidade, arquivo_paginas_visitadas, paginas_visitadas)

    # Suponha que 'paginas' seja uma lista de dicionários contendo informações sobre as páginas
    paginas = [
        {
            'links': links,  # Use os links extraídos
            'texto': 'Lorem ipsum dolor sit amet',  # Exemplo de texto da página
            'html': '<html><body><h1>Lorem ipsum</h1></body></html>',  # Exemplo de HTML da página
            'data_publicacao': '2023-05-15',  # Exemplo de data de publicação da página
            'autoreferencia': False  # Exemplo de autoreferência da página
        }
        # Adicione mais páginas conforme necessário
    ]

    # Termos buscados
    termos_buscados = ['Lorem', 'ipsum']

    # Classificar as páginas
    paginas_classificadas = classificar_paginas(paginas, termos_buscados)

