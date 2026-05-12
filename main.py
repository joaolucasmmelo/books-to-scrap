import requests
from bs4 import BeautifulSoup
import json

dados_para_json = []
url_base = 'https://books.toscrape.com/'

paginas_para_extrair = 2
for i in range(1,paginas_para_extrair + 1):
    url_page = url_base + f'catalogue/page-{str(i)}.html'
    response = requests.get(url_page)

    soup = BeautifulSoup(response.text, 'html.parser')
    livros = soup.find_all('article', class_ = 'product_pod')

    for livro in livros:
        livro_link = livro.find('div', class_ = 'image_container').find('a')['href'].replace('../', '')
        
        url_livro = f"https://books.toscrape.com/catalogue/{livro_link}"
        titulo = livro.find('h3').find('a')['title']
        preco = livro.find('div', class_ = 'product_price').find('p', class_ = 'price_color').text
        estrelas = livro.find('p')['class'][1]
        disponibilidade = livro.find('div', class_ = 'product_price').find('p', class_ = 'instock availability').text.strip()

        response_livro = requests.get(url_livro)
        soup_livro = BeautifulSoup(response_livro.text, 'html.parser')

        livro_content = soup_livro.find('article', class_ = 'product_page').find('div', class_ = 'row')

        quantidade_disponivel = livro_content.find('div', class_ = 'product_main').find('p', class_ = 'instock availability').text.strip()
        link_imagem = livro_content.find('img')['src'].replace('../../', '')
        url_imagem = f'https://books.toscrape.com/{link_imagem}'

        livro_atual = {
            'Titulo': titulo,
            'Preco': preco,
            'Estrelas': estrelas,
            'Link': url_livro,
            'Disponivel': disponibilidade,
            'Quantidade': quantidade_disponivel,
            'Imagem': url_imagem
        }

        dados_para_json.append(livro_atual)

with open('resultados_livros.json', 'w', encoding='utf-8') as arquivo:
    json.dump(dados_para_json, arquivo, indent=4, ensure_ascii=False)