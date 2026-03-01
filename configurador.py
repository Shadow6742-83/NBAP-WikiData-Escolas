def inicializar(formatar_nome):
    
    import platform
    import os
    import subprocess
    pasta_atual = os.path.dirname(os.path.abspath(__file__))
    os.chdir(pasta_atual)
    pwb_continue = False
    
    while not pwb_continue:    
        try:
            import pywikibot

            
            # A função PageGenerator interpreta a consulta SPARQL e retorna objetos pywikibot; WbTime é necessário
            # para processar datas no formato do Wikidata

            from pywikibot import pagegenerators, WbTime, WbQuantity, ItemPage
            from pywikibot.exceptions import OtherPageSaveError
           
            
            
            
            # Definindo o site (wikidata)
            pywikibot.config.user_agent = "NBAP 2.1 (BETA)"
            site = pywikibot.Site("wikidata", "wikidata")
            repo = site.data_repository()
            username = site.user()
            #site.user_agent = "NBAP 2.0"


            if username:
                print (f"Olá, {username}!")
                pwb_continuar = True
            else:
                user_login = input("Você não está logado no pywikibot.\nGostaria de se conectar? (S/n)\n: ")

                if user_login == '' or user_login == 'S' or user_login == 's':
                    input("Caso não saiba como se conectar, aqui vai uma rápida explicação!\nPara usar esse script, você precisar ter uma conta na wikidata (acesse https://www.wikidata.org para mais informações).\nSomente após a criação, você deverá continuar esse script!!\nDepois de criado a conta, você deverá apertar qualquer tecla e selecionar a Wikidata, nas proximas duas vezes que ela aparecer, após isso, você deverá informar o nome de usuario da sua conta da Wikidata.\nApós essa etapa, deverá ser pedido a sua senha da Wikidata, para que as informações alteradas por aqui sejam feitas por \"você\". Logo depois de ter se conectado, o script executará normalmente!")
                    print("Logando!")
                    os.system(f"python {pasta_atual}/core/pwb.py generate_user_files") 
                    os.system(f"python {pasta_atual}/core/pwb.py login")
                    print("Logado!")
                    username = site.user()
                    
                    print (f"Olá, {username}!")
                    pwb_continuar = True
                
                else:
                    print("Infelizmente, o script não pode continuar")
                    quit

        except ImportError:
            sistema = platform.system()
            versao = None
            
            if sistema == 'Linux':
                try:
                    with open('/etc/os-release', 'r') as f:
                        conteudo = f.read()

                        if ('ID=arch' or 'ID_LIKE=arch') in conteudo:
                            versao = "arch"
                            resposta = formatar_nome(input('Você está usando um sistema baseado em Arch Linux, e parece que não tem Pywikibot instalado (O que é necessario).\nGostaria de instalar? (S/n)\n: '))
                            
                            if resposta == '' or resposta == 'S':
                                git_chk = os.system("git --version > /dev/null 2>&1")

                                # Contraditorio? sim, mas descobri que o valor que retorna é a quantidade de erros que o comando teve, ou algo do tipo, então está certo!
                                if not git_chk:
                                   os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt --break-system-packages && pip install pywikibot --break-system-packages")
                                else:
                                    input("Parece que você não tem o git instalado, baixando a versão atual e instalando.\nPressione qualquer tecla para continuar.")
                                    os.system("sudo pacman -S --noconfirm git")
                                    os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt --break-system-packages && pip install pywikibot --break-system-packages")
                                    
                            else:
                                print("Infelizmente, o script não pode continuar sem o Pywikibot!!")
                                exit
                                
                        elif ('ID=debian' or "ID_LIKE=debian") in conteudo:
                            versao = "debian"
                            resposta = formatar_nome(input('Você está usando um sistema baseado no Debian, e parece que não tem Pywikibot instalado (O que é necessario).\nGostaria de instalar? (S/n)\n: '))
                            
                            if resposta == '' or resposta == 'S':
                                git_chk = os.system("git --version > /dev/null 2>&1")
                                if not git_chk:
                                    os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt && pip3 install pywikibot ")
                                else:
                                    input("Parece que você não tem o git instalado, baixando a versão atual e instalando.\nPressione qualquer tecla para continuar.")
                                    os.system("sudo apt install git")
                                    os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt && pip3 install pywikibot ")
                                    
                            else:
                                print("Infelizmente, o script não pode continuar sem o Pywikibot!!")
                                exit

                        
                except FileNotFoundError:
                    
                    os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt && pip install pywikibot")

            elif sistema == 'Windows':
                resposta = formatar_nome(input("Você está usando Windows e não tem pywikibot instalado (O que é necessario).\nGostaria de instalar? (S/n)\n: "))

                if resposta == '' or resposta == 'S':
                    git_chk = os.system("git --version > nul 2>&1")
                    if not git_chk:
                        os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt && pip install pywikibot")

                    else:
                        input("Parece que você não tem o git instalado, baixando a versão atual e instalando.\nPressione qualquer tecla para continuar.")
                        os.system("winget install --id Git.Git -e --source winget")
                        os.system("git clone https://gerrit.wikimedia.org/r/pywikibot/core.git && cd core && git submodule update --init && pip install -r requirements.txt && pip install pywikibot")
                        
    return site, repo 
