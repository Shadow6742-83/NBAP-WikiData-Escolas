# Tudo após "#" é um comentário

# Esse código foi desenvolvido para criar itens, no Wikidata, para escolas brasileiras que ainda não existem
# neste projeto. Utiliza, como fonte, o Censo Escolar de 2022. Para isso, segue três etapas:
# 1) A partir de um arquivo contendo dados do Censo, obtém os dados das escolas;
# 2) Realiza uma query (SPARQL) para conferir se a escola já existe no Wikidata;
# 3) Caso não exista, cria o item para a escola, contendo: "rótulo", "descrição", "instância de", "país" e "Código INEP";
# As três fases são realizadas em loop, até finalizar o arquivo fonte.

# Definindo funções

# Função para adicionar declarações







# Vamos trabalhar com pywikibot que é uma biblioteca, logo, precisamos importá-la
import pywikibot

# A função PageGenerator interpreta a consulta SPARQL e retorna objetos pywikibot; WbTime é necessário
# para processar datas no formato do Wikidata
from pywikibot import pagegenerators, WbTime, WbQuantity, ItemPage
from pywikibot.exceptions import OtherPageSaveError
import re
import sys
import time
import itertools

if not hasattr(time, 'original_sleep'):
    time.original_sleep = time.sleep
    time.sleep = animacao_espera

# Definindo o site (wikidata)
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
site.user_agent = "NBAP 2.0"

# Precisamos que o programa abra o arquivo fonte, e armazene seu conteúdo em uma variável para que possamos usá-lo
# Nesse caso, a variável será arquivo_csv

def criar_escolas(nome, codigo_inep, codigo_municipio, municipio, estudantes, professores, localizacao, localizacao_diferenciada, coordenadas_latitude, coordenadas_longitude, queima_lixo, separa_lixo, esgoto_fossa_comum, esgoto_inexistente, esgoto_rede, esgoto_fossa_septica, energia_gerador, energia_publica, energia_renovavel, adicionar_declaracao, energia_inexistente):
    # Etapa 2: realizar a consulta para verificar e existência (ou não) de um item

    # Nesta variável, vamos armazenar nossa query

    print(f"A escola {nome} ainda não existe no Wikidata. Prosseguindo para criação do item.")

    consulta_municipio = "select ?item where{ ?item wdt:P1585 '"+ codigo_municipio +"'  . }"

    municipio_item = pagegenerators.WikidataSPARQLPageGenerator(query=consulta_municipio,site=site)

    municipio_ID = str(next(iter(municipio_item), None)).replace("[[wikidata:", "")

    municipio_ID = str(municipio_ID).replace("]]", "")

    # Etapa 3: caso o item ainda não exista (conforme verificado na etapa 2), criá-lo        
        
    # Nesta variável (array), vamos armazenar as informações que gostaríamos de adicionar em nosso item
    dados = {
        'labels': {
        'en':  nome,
        'pt':  nome ,
    },
        'descriptions': {
        'en': 'school located in ' + municipio,
        'pt': 'escola localizada em ' + municipio,
        }
    }

    #Essa variavel vai nos ajudar a corrigir o bug do valor "Escola"        
    mapa_tipo_escola = {
        '1': "Q134739441",
        '2': "Q134739026",
        '3': "Q133804953",
        '0-1': "Q3914",        # localizacaoDiferenciada=0 e localizacao=1
        '0-2': "Q19855165",    # localizacaoDiferenciada=0 e localizacao=2
    }

    # Gera chave combinada para os casos especiais
    chave = (
        f"{localizacao_diferenciada}-{localizacao}"
        if localizacao_diferenciada == '0'
        else localizacao_diferenciada
    )

    # Busca no dicionário, ou retorna None se não existir
    tipo_escola = mapa_tipo_escola.get(chave)
        
    #Verifica se queima ou separa o lixo
    if queima_lixo == '1':
        queima_lixo_ID = 'Q133235'
    else:
        queima_lixo_ID = None

    if separa_lixo == '0':
        separa_lixo_ID = 'Q135276205'
    elif separa_lixo == '1':
        separa_lixo_ID = 'Q931389'
    else:
        separa_lixo_ID = None

    esgoto_fossa_comum_ID = None
    esgoto_fossa_septica_ID = None
    esgoto_rede_ID = None    
        
    if esgoto_inexistente == '1':
        esgoto_prop = 'P6477'

    elif esgoto_inexistente == '0':
        esgoto_prop = 'P912'
        
        if esgoto_fossa_comum == '1':
            esgoto_fossa_comum_ID = 'Q135336657'

        if esgoto_fossa_septica== '1':
            esgoto_fossa_septica_ID = 'Q386300'

        if esgoto_rede == '1':
            esgoto_rede_ID = 'Q156849'      

    energia_publica_ID = None
    energia_gerador_ID = None
    energia_renovavel_ID = None
        
    if energia_inexistente == '1':
        energia_prop = 'P6477'

    elif energia_inexistente == '0':
        energia_prop = 'P912'

        if energia_publica == '1':
            energia_publica_ID = 'Q1096907'
            
        if energia_gerador == '1':
            energia_gerador_ID = 'Q135343942'

        if energia_renovavel == '1':
            energia_renovavel_ID = 'Q12705'    

    # Criar um novo item vazio
    item = pywikibot.ItemPage(repo)

    # Criar o item com labels e descrições
    item.editEntity(dados, summary=f'criando item sobre escola ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')

    # Adicionar "instância de" (P31) = tipo_escola
    adicionar_declaracao(item, 'P31', tipo_escola)

    # Adicionar "país" (P17) = Brasil (Q155)
    adicionar_declaracao(item, 'P17', 'Q155')

    # Adicionar município (P131)
    adicionar_declaracao(item, 'P131', municipio_ID)

    # Adicionar "Código INEP" (P11704) = código da escola (string)
    adicionar_declaracao(item, 'P11704', codigo_inep, valor_tipo='string')

    # Adiciona as informações de tratamento de lixo
    adicionar_declaracao(
        item = item,
        prop_id='P912',      #Instalações
        valor='Q180388',     #Gestão de resíduos sólidos
        qualificadores=[
            ('P1552', queima_lixo_ID, 'wikibase-item'),
            ('P1552', separa_lixo_ID, 'wikibase-item')           
        ]
    )

    # Adiciona as informações de Esgoto
    adicionar_declaracao(
        item = item,
        prop_id = esgoto_prop,
        valor = 'Q20127660',
        qualificadores=[
            ('P1552', esgoto_fossa_comum_ID, 'wikibase-item'),
            ('P1552', esgoto_fossa_septica_ID, 'wikibase-item'),
            ('P1552', esgoto_rede_ID, 'wikibase-item')
        ]
    )

    # Adicionando as informações de Energia Elétrica
    adicionar_declaracao(
        item = item,
        prop_id = energia_prop,
        valor = 'Q206799',
        qualificadores=[
            ('P1552', energia_publica_ID, 'wikibase-item'),
            ('P1552', energia_gerador_ID, 'wikibase-item'),
            ('P1552', energia_renovavel_ID, 'wikibase-item')
        ]
    )

    # Adicionando quantidade de estudantes
    if estudantes:
        adicionar_declaracao(
            item = item,
            prop_id = 'P2196',       # propriedade "número de alunos" no Wikidata
            valor = int(estudantes),
            valor_tipo = 'quantity',
            qualificadores=[
                ('P585', pywikibot.WbTime(year=2023, precision=9), 'time')
            ]
        )

    # Adicionando quantidade de professores
    if professores:
        adicionar_declaracao(
            item = item,
            prop_id = 'P10610',       # propriedade "número de professores" no Wikidata
            valor = int(professores),
            valor_tipo = 'quantity',
            qualificadores=[
                ('P585', pywikibot.WbTime(year=2023, precision=9), 'time')
            ]
        )      

    # Adicionando dados sobre coordenadas
    if coordenadas_latitude and coordenadas_longitude:
        adicionar_declaracao(
            item = item,
            prop_id = 'P625',
            valor = {
                'latitude': coordenadas_latitude,
                'longitude': coordenadas_longitude
            },
            valor_tipo = 'coordinate'
        )

    print(f'Item criado para a escola {nome} (código INEP: {codigo_inep})')


