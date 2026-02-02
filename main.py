def adicionar_declaracao(item, prop_id, valor, valor_tipo='wikibase-item', qualificadores = None):
    declaracao = pywikibot.Claim(repo, prop_id)
    
    # Define o valor da declaração
    if valor_tipo == 'wikibase-item':
        target = pywikibot.ItemPage(repo, valor)
        declaracao.setTarget(target)
    elif valor_tipo == 'string':
        declaracao.setTarget(str(valor))
    elif valor_tipo == 'coordinate':
        declaracao.setTarget(pywikibot.Coordinate(
            lat=valor['latitude'],
            lon=valor['longitude'],
            precision=0.0001
            )
        )
    elif valor_tipo == 'quantity':
        declaracao.setTarget(pywikibot.WbQuantity(
            amount=valor,
            site=site
            )
        )
    elif valor_tipo == 'time':
        declaracao.setTarget(valor)
    else:
        raise ValueError('Tipo de valor não suportado')

    # Adiciona os Qualificadores
    if qualificadores:
        for prop_q, val_q, type_q in qualificadores:
            if val_q is None:
                continue # Pula se o valor não existir

            qual = pywikibot.Claim(repo, prop_q)

            if type_q == 'wikibase-item':
                target = pywikibot.ItemPage(repo, val_q)
                qual.setTarget(target)
            elif type_q == 'string':
                qual.setTarget(str(val_q))
            elif type_q == 'coordinate':
                qual.setTarget(pywikibot.Coordinate(
                    lat=val_q['latitude'],
                    lon=val_q['longitude'],
                    precision=0.0001
                )
            )
            elif type_q == 'quantity':
                qual.setTarget(pywikibot.WbQuantity(
                    amount=val_q,
                    site=site
                )
            )
            elif type_q == 'time':
                qual.setTarget(val_q)
            else:
                raise ValueError('Tipo de valor não suportado')

            declaracao.addQualifier(qual)
        
    # Adiciona sempre a mesma referência (Censo Escolar 2023, com a mesma data de acesso)
    # Adiciona referência: P248 (afirmado em) → Q133805362
    ref_fonte = pywikibot.Claim(repo, 'P248')
    item_fonte = pywikibot.ItemPage(repo, 'Q133805362')
    ref_fonte.setTarget(item_fonte)

    # Adiciona referência: P813 (data de consulta) → 10/07/2025
    data_consulta = pywikibot.WbTime(year=2025, month=7, day=10)
    ref_data = pywikibot.Claim(repo, 'P813')
    ref_data.setTarget(data_consulta)
        
    # Anexa as referências na declaração
    declaracao.addSources([ref_fonte, ref_data])
    if prop_pid is None:
        summaryis = f'adicionando propriedades, referências e qualificadores ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])'
    else:
        summaryis = f'editando e atualizando propriedades, referências e qualificadores ([[v:pt:Geografia para professores/Projeto Wikidata na Escola|Projeto Wikidata na Escola]] - [[Wikidata:WikiProject Brasil Escolas|WikiProjeto Brasil Escolas]])'
    # Adiciona a declaração ao item"
    item.addClaim(declaracao, summary=summaryis)

# 2. Nossa função de animação com contagem regressiva
def animacao_espera(segundos):
    # O Pywikibot às vezes passa valores muito pequenos, ignoramos se for < 0.5s
    if segundos < 0.5:
        time.original_sleep(segundos)
        return

    spinner = itertools.cycle(['|', '/', '-', '\\'])
    fim = time.time() + segundos
    
    while time.time() < fim:
        restante = round(fim - time.time(), 1)
        sys.stdout.write(f"\rAguardando... {next(spinner)} {restante}s faltando   ")
        sys.stdout.flush()
        time.original_sleep(0.1)
    
    sys.stdout.write(f"\rAguardando... Pronto!                          \n")

#Essa função é utilizada para formatar o nome das escolas,
#Existe função nativa, porém tem efeito estranho em "da", "de", "do", "das", "dos", "e".
def formatar_nome(nome):
    minusculas = ['da', 'de', 'do', 'das', 'dos', 'e']
    correcoes = {
        'educacao': 'Educação',
        'sao': 'São',  
        'colegio': 'Colégio',
        'tecnico': 'Técnico',
        'tecnologico': 'Tecnológico',
        'basico': 'Básico',
        'cei': 'CEI',
        'cmei': 'CMEI',
        'pre': 'Pré',
        'nucleo': 'Núcleo',
        ' iv': ' IV',
        'iii': 'III',
        'ii': 'II',
        'basica': 'Básica',
        'instituicao': 'Instituição',
        'fundacao': 'Fundação',
        'associacao': 'Associação',
        'acao': 'Ação',
        'servico': 'Serviço',
        'esperanca': 'Esperança',
        'lapis': 'Lápis',
        'espaco': 'Espaço',
        'crianca': 'Criança',
        'ceu': 'Céu',
        'pe': 'Pé',
        'valorizacao': 'Valorização',
        'comunitario': 'Comunitário',
        'tradicao':'Tradição',
        'simao':'Simão',
        'jose':'José',
        'joao':'João',
        'coracao':'Coração',
        'conceicao':'Conceição'
    }

    palavras = nome.lower().split()
    resultado = []
    ultima_palavra = None

    for i, palavra in enumerate(palavras):
        if palavra in correcoes:
            palavra_corrigida = correcoes[palavra]
        elif palavra in minusculas and i != 0:
            palavra_corrigida = palavra
        else:
            palavra_corrigida = palavra.capitalize()

        # Evitar repetição da mesma palavra consecutiva (inclusive preposições)
        if palavra_corrigida != ultima_palavra:
            resultado.append(palavra_corrigida)
            ultima_palavra = palavra_corrigida
    
    return ' '.join(resultado)

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
from createNewSchool import criar_escolas
from editSchool import editar_escolas
# Etapa 1: obter os dados da escola de um arquivo fonte

# Definindo qual é o arquivo fonte (com os dados que iremos importar)
arquivo_fonte = 'microdados_ed_basica_2023_sc_resumido.csv'

# Definindo o site (wikidata)
site = pywikibot.Site("wikidata", "wikidata")
repo = site.data_repository()
site.user_agent = "NBAP 2.0"


with open(arquivo_fonte, newline='', encoding='utf-8') as arquivo_csv:
    
    # Vamos usar a classe DictReader, da biblioteca csv que importamos, para processar nosso arquivo fonte,
    # que está no formato .csv. Cada linha de conteúdo será armazenada como um objeto, com cabeçalho
    leitor = csv.DictReader(arquivo_csv, delimiter=';')
    
    # Cada objeto do arquivo (cada linha), será armazenado na variável 'linha', e para cada linha, faremos o seguinte:
    # Importante: esse é o loop de nosso código, onde para cada linha (cada escola) o programa repetirá todas as
    # instruções abaixo:
    for linha in leitor:
        
        # Armazenar os valores em novas variáveis, para reutilizar depois, nos passos 2 e 3
        nome = formatar_nome(linha['NO_ENTIDADE'])
        codigo_inep = linha['CO_ENTIDADE']
        municipio = linha['NO_MUNICIPIO']
        codigo_municipio = linha['CO_MUNICIPIO']
        estudantes = linha['QT_MAT_BAS']
        professores = linha['QT_DOC_BAS']
        localizacao = linha['TP_LOCALIZACAO']
        localizacao_diferenciada = linha['TP_LOCALIZACAO_DIFERENCIADA']        
        queima_lixo = linha['IN_LIXO_QUEIMA']
        separa_lixo = linha['IN_TRATAMENTO_LIXO_SEPARACAO']
        esgoto_inexistente = linha['IN_ESGOTO_INEXISTENTE']
        esgoto_fossa_comum = linha['IN_ESGOTO_FOSSA_COMUM']
        esgoto_fossa_septica = linha['IN_ESGOTO_FOSSA_SEPTICA']
        esgoto_rede = linha['IN_ESGOTO_REDE_PUBLICA']
        energia_inexistente = linha['IN_ENERGIA_INEXISTENTE']
        energia_publica = linha['IN_ENERGIA_REDE_PUBLICA']
        energia_gerador = linha['IN_ENERGIA_GERADOR_FOSSIL']
        energia_renovavel = linha['IN_ENERGIA_RENOVAVEL']
        coordenadas_latitude = linha['COORDENADAS_LAT']
        coordenadas_longitude = linha['COORDENADAS_LON']
        # Final da Etapa 1


        consulta = "SELECT ?item ?itemLabel  WHERE { ?item wdt:P11704 '" + codigo_inep + "' . }"
        # Checando se existe um item ou não
        escolas = list(pagegenerators.WikidataSPARQLPageGenerator(query=consulta, site=site))

        prop_pid = None
        continuar = None
        if escolas:
            editar_escolas(nome, codigo_inep, codigo_municipio, municipio, estudantes, professores, localizacao, localizacao_diferenciada, coordenadas_latitude, coordenadas_longitude, queima_lixo, separa_lixo, esgoto_fossa_comum, esgoto_inexistente, esgoto_rede, esgoto_fossa_septica, energia_gerador, energia_publica, energia_renovavel, adicionar_declaracao, escolas, continuar, energia_inexistente)

        if not escolas:
            try:
                
                criar_escolas(nome, codigo_inep, codigo_municipio, municipio, estudantes, professores, localizacao, localizacao_diferenciada, coordenadas_latitude, coordenadas_longitude, queima_lixo, separa_lixo, esgoto_fossa_comum, esgoto_inexistente, esgoto_rede, esgoto_fossa_septica, energia_gerador, energia_publica, energia_renovavel, adicionar_declaracao, energia_inexistente)

            except OtherPageSaveError as e:
                # Se falhar por duplicata, vamos tentar pegar o ID que o erro nos deu
                error_msg = str(e)
                if "modification-failed" in error_msg:
                    # Extrai o QID da mensagem de erro (ex: Q135467635)
                    match = re.search(r'Q\d+', error_msg)
                    if match:
                        qid_existente = match.group()
                        print(f"AVISO: O item já existe ({qid_existente}). Carregando item existente...")
                        item = pywikibot.ItemPage(repo, qid_existente)
                    else:
                        print("Erro de modificação, mas não consegui extrair o QID.")
                        raise e

                    # Aqui checamos se tem codigo INEP
                    claim = checar(item.id, 'P11704')

                    # Nesse "if" checamos se não temos o codigo na escola
                    if not claim:

                        print("Escola não tem codigo INEP, Adicionando agora!")
                        
                        # Adicionar "Código INEP" (P11704) = código da escola (string)
                        adicionar_declaracao(item, 'P11704', codigo_inep, valor_tipo='string')

                    continuar = True
                    editar_escolas(nome, codigo_inep, codigo_municipio, municipio, estudantes, professores, localizacao, localizacao_diferenciada, coordenadas_latitude, coordenadas_longitude, queima_lixo, separa_lixo, esgoto_fossa_comum, esgoto_inexistente, esgoto_rede, esgoto_fossa_septica, energia_gerador, energia_publica, energia_renovavel, adicionar_declaracao,  escolas, continuar,  energia_inexistente)
