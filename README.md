<p align="center">
  <img src="Logo WikiData na Escola - SC (sem fundo).png" alt="Logo do Projeto" width="200"/>
</p>

<h1 align="center">📚 Projeto NBAP Wikidata na Escola – Mapeando Escolas de Santa Catarina na Wikidata</h1>

<p align="center">
Utilizando o Censo Escolar para mapear todas as escolas na <b>WikiData</b>.
</p>

---

## 📝 Introdução
Nosso trabalho teve como foco dar **Representatividade** as escolas de Santa Catarina na Wikidata, uma plataforma global de dados estruturados e colaborativa. Por não haver muitas escolas cadastradas na WikiData, era difícil fazer análises abertas sobre a educação básica, a partir disso, surgiu a proposta desse projeto (sendo filho de um projeto maior), automatizando com os dados do Censo Escolar e a programação em **Python** e **SPARQL**

## 🎯 Objetivos
Criar escolas na Wikidata, nas quais não existiam, utilizando-se desses passos:
  - Extrair e tratar os dados a partir de um arquivo fonte (Censo Escolar), garantindo a qualidade e consistência das informações.
  - Verificar se cada instituição existe na Wikidata por meio de consultas em SPARQL, a fim de evitar duplicidades.
  - Criar novos itens no Wikidata para as escolas não encontradas

## 🛠️ Metodologia
O projeto foi feito concluindo esses quatro passos principais:
  1. **Capacitação** – Foi realizada oficinas online e presenciais para introduzir a Wikidata, Python, SPARQL e o conceito dos dados estruturados aos alunos do projeto.
  2. **Coleta de Dados** – Extração dos microdados do **Censo Escolar de 2023**, filtrando as informações importantes de cada instituição. 
  3. **Programação** – Desenvolvimento e execução do script em Python para automatizar a criação de itens no Wikidata, por meio deste repositório.  
  4. **Escrita do resumo** – Após o fim da etapa anterior, foi escrito um resumo, pelos próprios alunos, refletindo sobre o trabalho feito e sistematizando sobre os resultados.

## 📊 Resultados
Foram criadas 6.590 instituições na Wikidata, desde escolas municipais, estaduais, quilombolas, rurais e privadas, contendo dados de **Saneamento Básico**, **Tratemento de lixo** e **Tipo de energia elétrica**
O projeto mostrou que a Wikidata foi mais interativa que vários sites governamentais (Exemplos: Educação na Palma da Mão, Tribunal de Contas do Estado de Santa Catarina - TCE/SC)

<p align="center">
  <img src="image.png" alt="Logo do Projeto" width="600"/>
</p>
<p align="center">
Todas as escolas de Santa Catarina, nas quais não tem acesso a rede de esgoto.
(Veja a consulta em https://w.wiki/FCPs)
</p>

## 🛠 Explicando o Repositório e o Código
Algumas partes teremos que explicar como funciona a Wikidata, para mais informações, veja o ultimo item da nossas referências, pois lá é mais completo.
- **createnewschool.py** - Esse é o script principal, ele utiliza o pywikibot para criar instancias na Wikidata e fazer consultas em SPARQL, e csv para ler os arquivos do Censo Escolar organizados no arquivo fonte. No inicio do arquivo está as funções, que são:
  - **adicionar_declaracao(item, prop_id, valor, valor_tipo='wikibase-item', qualificadores = None):** Vamos explicar com calma essa função.
  Como diz o nome da função, ela adiciona uma declaração na wikidata, ela funciona como I.P.V. (Item, Propriedade e Valor).

    - ```item``` é o item que você está adicionando na wikidata (instancia da escola).
      
    - O ```prop_id``` é a prorpiedade que você irá adicionar (exemplos: P912 é "instalações", P31 é "instância de").
    
    - O ```valor``` é o valor (exemplos: P17 (País), Q155 (Brasil), P é a Propriedade, enquanto o Q é o valor. Isso mostra que a Escola (Item) tem uma declaração na qual mostra que ela fica localizada no país (P17, Propriedade "País") Brasil (Q155, Valor "Brasil")).
    
      Exemplo um pouco dificil? Ok! Vamos para um mais fácil!.

      Exemplo 2: ```adicionar_declaracao(item, 'P31', 'Q3914')``` Aqui é um pouco mais fácil, O código mostra, que ele irá adicionar na Escola (Item) que ela é uma "Instância de" (P31, Propriedade) de "Escola" (Q3914, Valor).
   
    - Já ```valor_tipo='wikibase-item'``` é o tipo de valor que a variável ```valor``` tem.
    Por exemplo: se o valor dela for ```coordinate``` ela vai ser tratada como uma coordenada, se for uma ```string```, ela vai ser tratada como um texto e assim por diante. Caso não for um valor valido, o código gera um erro.

    - ```qualificadores = None```, Aqui é mais complexo, pois a estrutura muda um pouco.
    Se você quer adicionar ao Item, que a Escola tem Coleta Seletiva, você coloca P912 (Instalações) na propriedade e Q180388 (Gestão de Resíduos Sólidos) nos valores, mas... espera...? Não está muito vago?
    
      Está sim, mas pra corrigir isso, existe os qualificadores!

      O formato I.P.V. (Item, Propriedade e Valor) pode ser levemente alterado se o valor também se tornar um Item enquanto ele ainda é um valor, e ele irá precisar de uma nova Propriedade e de um novo Valor.

       Exemplo:
          <pre> ```   adicionar_declaracao(
                        item = item,
                        prop_id='P912',      
                        valor='Q180388',     
                        qualificadores=[
                        ('P1552', 'Q931389', 'wikibase-item')           
                        ]
                      )```
          </pre>

        No exemplo acima, o Item é a Escola, a Propriedade é "Instalações" e o Valor é Gestão de Resíduos Sólidos, porém o Valor se torna um Item para abrigar a Propriedade "P1552" (Tem Característica) e ter um valor "Q931389" (Coleta Seletiva), enquanto ele mesmo é um valor do Item "Escola".

  - **formatar_nome(nome):** Essa Função é muito mais simples, ela somente corrige os nomes do arquivo do Censo Escolar.

- **Pasta Dados:** Aqui estão todos os dados do Censo Escolar 2023 divididos em lotes, pois cada estudante enviou um de cada vez pelo seu proprio computador.

## 📚 Referências

1. BRASIL. Instituto Nacional de Estudos e Pesquisas Educacionais Anísio Teixeira. *Censo escolar da educação básica 2023: microdados*. Disponível no: [link](https://www.gov.br/inep/pt-br/acesso-a-informacao/dados-abertos/microdados/censo-escolar). Acesso em: 8 ago. 2025.  

2. OUTREACH DASHBOARD. *Wikidata na Escola*. Disponível no: [link](https://outreachdashboard.wmflabs.org/courses/EEB_Prof._Nicola_Baptista/Wikidata_na_Escola/home). Acesso em: 8 ago. 2025.  

3. SAMPAIO, R.C.; SABBATINI, M.; LIMONGI, R. *Diretrizes para o uso ético e responsável da Inteligência Artificial Generativa: um guia prático para pesquisadores*. São Paulo: Editora Intercom, 2024.  

4. SANTA CATARINA. *Educação na Palma da Mão*. Disponível no: [link](https://www.sed.sc.gov.br/educacao-na-palma-da-mao/). Acesso em: 8 ago. 2025.  

5. TRIBUNAL DE CONTAS DE SANTA CATARINA. *Painel de Infraestrutura das Escolas Catarinenses*. Disponível no: [link](https://tcesc.shinyapps.io/painelinfraestrutura/). Acesso em: 8 ago. 2025.  

6. WIKIDATA. *Introduction*. Disponível no: [link](https://www.wikidata.org/wiki/Wikidata:Introduction). Acesso em: 8 ago. 2025.  
