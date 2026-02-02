# Tudo após "#" é um comentário

# Esse código foi desenvolvido para criar itens, no Wikidata, para escolas brasileiras que ainda não existem
# neste projeto. Utiliza, como fonte, o Censo Escolar de 2022. Para isso, segue três etapas:
# 1) A partir de um arquivo contendo dados do Censo, obtém os dados das escolas;
# 2) Realiza uma query (SPARQL) para conferir se a escola já existe no Wikidata;
# 3) Caso não exista, cria o item para a escola, contendo: "rótulo", "descrição", "instância de", "país" e "Código INEP";
# As três fases são realizadas em loop, até finalizar o arquivo fonte.

# Definindo funções

def adicionador_rapido(item, prop_pid, coordenadas_latitude, coordenadas_longitude, estudantes, professores, queima_lixo_ID, separa_lixo_ID, esgoto_prop, esgoto_fossa_comum_ID, esgoto_fossa_septica_ID, esgoto_rede_ID, energia_prop, energia_publica_ID, energia_gerador_ID, energia_renovavel_ID):
    
    if (prop_pid == 'P912'):
        # Adiciona as informações de tratamento de lixo
        print("adicionando gestão de residuos solidos!")
            
        adicionar_declaracao(
            item = item,
            prop_id='P912',      #Instalações
            valor='Q180388',     #Gestão de resíduos sólidos
            qualificadores=[
                ('P1552', queima_lixo_ID, 'wikibase-item'),
                ('P1552', separa_lixo_ID, 'wikibase-item')           
            ]
        )

        if 'P912' in esgoto_prop:
            print("adicionando Tratamento de Esgoto!")
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
        if 'P912' in energia_prop:
            print("adicionando gestão de energia!")
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
    elif 'P2196' in prop_pid:
       
        # Adicionando quantidade de estudantes
        if estudantes:
            print("adicionando Quantidade de Alunos!")
            adicionar_declaracao(
                item = item,
                prop_id = 'P2196',       # propriedade "número de alunos" no Wikidata
                valor = int(estudantes),
                valor_tipo = 'quantity',
                qualificadores=[
                    ('P585', pywikibot.WbTime(year=2023, precision=9), 'time')
                ]
            )
        else:
            print("Essa escola não apresenta Quantidade de Professores no Censo de 2023!")
    elif 'P10610' in prop_pid:
        
        #Adicionando quantidade de professores
        if professores:
            print("adicionando Quantidade de Professores!")
            adicionar_declaracao(
                item = item,
                prop_id = 'P10610',       # propriedade "número de professores" no Wikidata
                valor = int(professores),
                valor_tipo = 'quantity',
                qualificadores=[
                    ('P585', pywikibot.WbTime(year=2023, precision=9), 'time')
                ]
            )
        else:
            print("Essa escola não apresenta Quantidade de Professores no Censo de 2023!")
    elif prop_pid == 'P625':
        
        # Adicionando dados sobre coordenadas
        if coordenadas_latitude and coordenadas_longitude:
            print("adicionando Coordenadas Geograficas!")
            adicionar_declaracao(
                item = item,
                prop_id = 'P625',
                valor = {
                    'latitude': coordenadas_latitude,
                    'longitude': coordenadas_longitude
                },
                valor_tipo = 'coordinate'
            )
        else:
            print("Essa escola não apresenta Coordenadas Geograficas no Censo de 2023!")



def checar(item_id, prop_id): 
    site = pywikibot.Site("wikidata", "wikidata")
    repo = site.data_repository()

    item = pywikibot.ItemPage(repo, item_id)
    item.get()
    
    cheque = item.claims.get(prop_id,[])

    return cheque
        



def editar_escolas(nome, codigo_inep, codigo_municipio, municipio, estudantes, professores, localizacao, localizacao_diferenciada, coordenadas_latitude, coordenadas_longitude, queima_lixo, separa_lixo, esgoto_fossa_comum, esgoto_inexistente, esgoto_rede, esgoto_fossa_septica, energia_gerador, energia_publica, energia_renovavel, adicionar_declaracao, escolas, continuar, energia_inexistente):

    if escolas or continuar:
        # Localiza exatamente o item da escola.
        if escolas:
            item = escolas[0]

        # Diz qual é a escola
        label_pt = item.labels.get("pt")
        print(item.id, label_pt)

        # Este codigo, altera o nome da escola corretamente, de acordo com a formatação na função "formatar_nome"
        if (label_pt != nome):
            item.editLabels(
                labels={
                        "pt": nome,
                        "en": nome
                         },
                summary=f'editando item sobre escola ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])'
            )
            print("Editando Nome")

        # Aqui faz uma checagem sobre o que a escola tem de ""Instalações", será muito util mais tarde!
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

        # Nesse exato momento, o script se preparar para checar se o Item na wikidata está atualizado!
        print("Checando!")

        # Aqui é criado um "For i in range", que resumindo, ele cria um loop enquanto a variavel "i", que é um valor inteiro, for menor que 6.
        # Ao fim do loop, se i for menor que 6, é incrementado o valor i (Ou seja, i se torna igual a i + 1).
        for i in range(6):

            # Aqui fazemos um sistema de interruptores (Switchs), que se i, que é o valor que estamos checando nesse switch, entrar em algum dos casos abaixo,
            # ele irá fazer algo conforme o seu valor.
            # a variavel "prop_pid" é a variavel que vai armazenar o valor da propriedade que queremos checar mais tarde
            match i:

                case 0:
                    prop_pid = 'P912'          # Instalações
            
                case 1:
                    if (esgoto_prop == 'P912'):
                        continue               # Aqui checamos se não é a mesma de instalações, para não duplicar a mesma informação da anterior

                    prop_pid = esgoto_prop
                case 2:
                    if (energia_prop == 'P912' or esgoto_prop == energia_prop):
                        continue               # Aqui é quase a mesma coisa, mas checamos se também não é igual ao do Esgoto
                    
                    prop_pid = energia_prop
                case 3:
                    prop_pid = 'P2196'         # Quantidade de Estudantes

                case 4:
                    prop_pid = 'P10610'        # Quantidade de Professores
                    
                case 5:
                    prop_pid = 'P625'          # Coordenadas Geograficas
                    

            # Aqui começamos de verdade o processo de checagem
            claim = checar(item.id, prop_pid)

            # Nesse "for" armazenamos as informações de "claim" em "cheque"
            for cheque in claim:

                
                valor_i = cheque.getTarget()

                if isinstance (valor_i, pywikibot.Coordinate):
                    lat = valor_i.lat
                    lon = valor_i.lon
                    if float(coordenadas_latitude) == lat and float(coordenadas_longitude) == lon:
                        
                        valor_f = f"{lat}, {lon}"
                        print(f"Tem Cordenadas: {valor_f}!")
                    else:
                        item.removeClaims([cheque], summary=f'removendo coordenadas desatualizadas ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')
                        adicionar_declaracao(
                        item,
                        prop_pid,
                        {
                            'latitude': coordenadas_latitude,
                            'longitude': coordenadas_longitude
                        },
                        valor_tipo = 'coordinate'
                        )
                        print(f"Coordenadas ({lat},{lon}) adicionadas!")
                       

                        
                elif isinstance(valor_i, WbQuantity):
                    valor_principal = valor_i.amount
                    
                    if prop_pid == 'P10610':
                        print(f"Quantidade de Professores:\n Wikidata:{valor_principal}\n Censo:{professores}")
                        if valor_principal != int(professores):
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
                    elif prop_pid == 'P2196':
                        print(f"Quantidade de Estudantes:\n Wikidata:{valor_principal}\n Censo:{estudantes}")
                        if valor_principal != int(estudantes):
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
                                
                if cheque.qualifiers:
                    
                    for qprop, qclaims in cheque.qualifiers.items():
                        for q in qclaims:
                            quali = q.getTarget()
                            if isinstance (quali, ItemPage):
                                valorq = quali.id
                                
                                match valor_i.id:

                                    case 'Q206799':
                                        
                                        if (prop_pid != energia_prop):
                                            print("Propriedade diferente\nEditando")
                                            item.removeClaims([cheque], summary=f'removendo propriedades de energia desatualizadas ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')
                                            adicionar_declaracao(item, energia_prop,'Q206799', valor_tipo='wikibase-item', qualificadores=[
                                                    ('P1552', energia_publica_ID, 'wikibase-item'),
                                                    ('P1552', energia_gerador_ID, 'wikibase-item'),
                                                    ('P1552', energia_renovavel_ID, 'wikibase-item')
                                                ]
                                            )
                                        elif (valorq != energia_gerador_ID and valorq != energia_publica_ID and valorq != energia_renovavel_ID):
                                            print("Qualificador de Energia diferente\nEditando")
                                            item.removeClaims([cheque], summary=f'removendo qualificadores de energia desatualizadas ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')
                                            adicionar_declaracao(item, energia_prop,'Q206799', valor_tipo='wikibase-item', qualificadores=[
                                                    ('P1552', energia_publica_ID, 'wikibase-item'),
                                                    ('P1552', energia_gerador_ID, 'wikibase-item'),
                                                    ('P1552', energia_renovavel_ID, 'wikibase-item')
                                                ]
                                            )

                                    case 'Q20127660':
                                        
                                        if (prop_pid != esgoto_prop):
                                            print("Propriedade diferente\nEditando")
                                            item.removeClaims([cheque], summary=f'removendo propriedades de esgoto desatualizadas ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')
                                            adicionar_declaracao(item, esgoto_prop,'Q20127660', valor_tipo='wikibase-item', qualificadores=[
                                                    ('P1552', esgoto_fossa_comum_ID, 'wikibase-item'),
                                                    ('P1552', esgoto_fossa_septica_ID, 'wikibase-item'),
                                                    ('P1552', esgoto_rede_ID, 'wikibase-item')
                                                ]
                                            )
                                        elif (valorq != esgoto_fossa_comum_ID and valorq != esgoto_fossa_septica_ID and valorq != esgoto_rede_ID): # alterar, ele não identifica mais de dois
                                            print("Qualificador de Esgoto diferente\nEditando")
                                            item.removeClaims([cheque], summary=f'removendo qualificadores de esgoto desatualizadas ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')
                                            adicionar_declaracao(item, esgoto_prop,'Q20127660', valor_tipo='wikibase-item', qualificadores=[
                                                ('P1552', esgoto_fossa_comum_ID, 'wikibase-item'),
                                                ('P1552', esgoto_fossa_septica_ID, 'wikibase-item'),
                                                ('P1552', esgoto_rede_ID, 'wikibase-item')
                                                ]
                                            )

                                    case 'Q180388':
                                        
                                        if (valorq != queima_lixo_ID and valorq != separa_lixo_ID):
                                            print("Qualificador de Lixo diferente\nEditando")
                                            item.removeClaims([cheque], summary=f'removendo qualificador de lixo desatualizado ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])')
                                            adicionar_declaracao(item, 'P912','Q180388', valor_tipo='wikibase-item', qualificadores=[
                                                ('P1552', queima_lixo_ID, 'wikibase-item'),
                                                ('P1552', separa_lixo_ID, 'wikibase-item'),
                                                ]
                                            )

                elif not isinstance(valor_i, pywikibot.Coordinate):
                    print("Não tem Qualificadores")

            if not claim:
                print(f"Não tem propriedades com {prop_pid}\nAdicionando propriedades!")
                
                prop_chk = ['P31', 'P17', 'P131']
                
                for i in range(len (prop_chk)):
                    check = checar(item.id, prop_chk[i])
                    if not check:
                        print(f"Não tem propriedades com {prop_chk[i]}\nAdicionando propriedades!")
                        match i:
                            case 0:
                                print("Adicionando Instancia de Escola")
                                # Adicionar "instância de" (P31) = tipo_escola
                                #Essa variavel vai nos ajudar a corrigir o bug do valor "Escola"        
                                mapa_tipo_escola = {
                                    '1': "Q134739441",
                                    '2': "Q134739026",
                                    '3': "Q133804953",
                                    '0-1': "Q3914",        # localizacaoDiferenciada=0 e localizacao=1
                                    '0-2': "Q19855165",    # localizacaoDiferenciada=0 e localizacao=2
                                }
                        
                                #Gera chave combinada para os casos especiais
                                chave = (
                                    f"{localizacao_diferenciada}-{localizacao}"
                                    if localizacao_diferenciada == '0'
                                    else localizacao_diferenciada
                                )
            
                                #Busca no dicionário, ou retorna None se não existir
                                tipo_escola = mapa_tipo_escola.get(chave)
                                 
                                adicionar_declaracao(item, 'P31', tipo_escola)
                            case 1:
                                print("Adicionando País")
                                #Adicionar "país" (P17) = Brasil (Q155)
                                adicionar_declaracao(item, 'P17', 'Q155')
                            case 2:
                                print("Adicionando Municipio")
                                #Adicionar município (P131)
                                consulta_municipio = "select ?item ?itemLabel where{ ?item wdt:P1585 '"+ codigo_municipio +"'  . }"

                                municipio_item = list(pagegenerators.WikidataSPARQLPageGenerator(query=consulta_municipio,site=site))

                                municipio_ID = municipio_item[0]
                                    
                                adicionar_declaracao(item, 'P131', municipio_ID.id)

                adicionador_rapido(item, prop_pid, coordenadas_latitude, coordenadas_longitude, estudantes, professores, queima_lixo_ID, separa_lixo_ID, esgoto_prop, esgoto_fossa_comum_ID, esgoto_fossa_septica_ID, esgoto_rede_ID, energia_prop, energia_publica_ID, energia_gerador_ID, energia_renovavel_ID)
                

# Início do script

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
# Vamos utilizar essa biblioteca para ler o arquivo fonte, que está salvo no formato csv
import csv
import subprocess
from editSchool import editar_escolas
# Etapa 1: obter os dados da escola de um arquivo fonte

# Definindo qual é o arquivo fonte (com os dados que iremos importar)
arquivo_fonte = 'microdados_ed_basica_2023_sc_resumido.csv'

# Definindo o site (wikidata)
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
site.user_agent = "NBAP 2.0"

