# %%

import requests, time, random, re, json, datetime, pytz, os

from prefect import flow, task
from bs4 import BeautifulSoup
from prefect_aws.s3 import S3Bucket
from load_credentials import Credentials

credenciais = Credentials()
base_url = credenciais.base_url["base_url"]
max_range = 100

def aguardar():
    delay = random.uniform(2, 5)
    print(f"Esperando {delay:.1f} segundos...")
    time.sleep(delay)

@task(retries=3, retry_delay_seconds=10, timeout_seconds=45)
def obter_html(url):

    response = requests.get(url, cookies=credenciais.cookies, headers=credenciais.headers, timeout=30)

    soup = BeautifulSoup(response.text, 'html.parser')

    return soup

@task(retries=2, retry_delay_seconds=5)
def extrair_links_anuncios(base_url):

    links = []

    for i in range(1, max_range + 1):
        url = f'{base_url}&o={i}'
        soup = obter_html(url)
        anuncios = soup.find_all('a', class_="olx-adcard__link")
        links_pagina = [link['href'] for link in anuncios if link.has_attr('href')]
            
        print(f"Encontrados {len(links_pagina)} anúncios")
            
        if len(links_pagina) == 0:
            print("Nenhum anúncio encontrado. Interrompendo...")
            break

        links.extend(links_pagina)

        aguardar()

    print("Interrompido.")

    return links

@task(retries=2, retry_delay_seconds=3)
def extrair_info_imovel(link):

    imovel = {}

    soup = obter_html(link)

    # Código do anúncio
    imovel['cod_anuncio'] = link.split("-")[-1]

    # Título e Descrição
    div_desc = soup.find('div', id='description-title').find_all({'span': 'data-ds-component="DS-Text'})

    if div_desc:
        imovel['titulo'] = div_desc[0].text
        imovel['descricao'] = div_desc[1].text    

    else:
        imovel['titulo'] = "N/A"
        imovel['descricao'] = "N/A"

    # Valores de Aluguel, IPTU e Condomínio
    span_precos = soup.find('div', id='price-box-container').find_all('span')

    if span_precos:
        itens = [valor.text for valor in span_precos] 
        precos = {}
        chave = None
        valor = None

        for item in itens:
            if item in ['Aluguel', 'Condomínio', 'IPTU']:
                chave = item
            elif item.startswith("R$"):
                valor = item
            if chave == None:
                continue

            precos[chave] = valor

        imovel['precos'] = precos 

    else:
        imovel['precos'] = "N/A"

    # Endereço do imóvel
    span_localizacao = soup.find('div', id='location').find_all('span')[1:-2]

    if span_localizacao:
        imovel['endereco'] = [end.text for end in span_localizacao]

    else:
        imovel['endereco'] = "N/A"

    # Características do imóvel e do condomínio
    span_pagina = soup.find_all({'span': 'data-ds-component="DS-Text'})

    texto_pagina = [texto.text for texto in span_pagina if texto.text not in 'Fechar janela de diálogo']

    texto_pagina = "|".join(texto_pagina)

    if texto_pagina:
        try: 
            imovel['carac_imovel'] = list(set(texto_pagina.split("Características do imóvel")[1].split("|")))
            imovel['carac_cond'] = list(set(texto_pagina.split("Características do condomínio")[1].split("|")))

        except:
            imovel['carac_imovel'] = "N/A"
            imovel['carac_cond'] = "N/A"

    # Data do anúncio
    regex_data = r'\b\d{2}/\d{2}\s*às\s*\d{2}:\d{2}\b'

    data = re.findall(regex_data, texto_pagina)        
    if data:
        imovel['data_anuncio'] = str(data[0])

    else:
        imovel['data_anuncio'] = "N/A"

    return imovel

@task(retries=2, retry_delay_seconds=3)
def scrape(links):

    dados_completos = []
    
    for link in links:
        resultado = extrair_info_imovel(link)
        dados_completos.append(resultado)
        aguardar()

    return dados_completos

@task
def upload_arquivo_s3(arquivo):

    s3_bucket = S3Bucket(
        bucket_name="olx-raw",
        credentials=credenciais.aws_credentials
    )

    s3_bucket_path = s3_bucket.upload_from_path(
        from_path=arquivo,
        to_path=f"raw/{os.path.basename(arquivo)}"
    )

    print(s3_bucket_path)

@flow()
def pipeline_olx():

    links = extrair_links_anuncios(base_url)

    dados = scrape(links)
    
    data = datetime.datetime.now(pytz.timezone('America/Sao_Paulo'))
    nome_arquivo = f'imoveis_{data}.json'

    with open(nome_arquivo, 'w') as f:
        json.dump(dados, f)

    upload_arquivo_s3(nome_arquivo)

if __name__ == "__main__":

    pipeline_olx()