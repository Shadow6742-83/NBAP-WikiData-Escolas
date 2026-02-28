def inicializar():
    
    import platform
    import os
    import subprocess
    try:
        import pywikibot

                
        # A função PageGenerator interpreta a consulta SPARQL e retorna objetos pywikibot; WbTime é necessário
        # para processar datas no formato do Wikidata

        from pywikibot import pagegenerators, WbTime, WbQuantity, ItemPage
        from pywikibot.exceptions import OtherPageSaveError
       
        
        
        
        # Definindo o site (wikidata)
        site = pywikibot.Site("wikidata", "wikidata")
        repo = site.data_repository()
        username = site.user()
        site.user_agent = "NBAP 2.0"


        if username:
            print (f"Olá, {username}!")
        else:
            user_login = input("Você não está logado no pywikibot.\nGostaria de se conectar? (S/n)\n: ")

            if user_login == '' or user_login == 'S' or user_login == 's':
                input("Caso não saiba como se conectar, aqui vai uma rápida explicação!\nPara usar esse script, você precisar ter uma conta na wikidata (acesse https://www.wikidata.org para mais informações).\nSomente após a criação, você deverá continuar esse script!!\nDepois de criado a conta, você deverá apertar qualquer tecla e selecionar a Wikidata, nas proximas duas vezes que ela aparecer, após isso, você deverá informar o nome de usuario da sua conta da Wikidata.\nApós essa etapa, deverá ser pedido a sua senha da Wikidata, para que as informações alteradas por aqui sejam feitas por \"você\". Logo depois de ter se conectado, o script executará normalmente!")
                os.system("pwb generate-userconfig")
                os.system("pwb login")
                username = site.user()
                print (f"Olá, {username}!")
                
                
                    
            else:
                print("Infelizmente, o script não pode continuar")
                quit

    except ImportError:
        sistema = platform.system()
        versao = None
        if sistema == 'Linux':
            with open('/etc/os-release', 'r') as f:
                conteudo = f.read()

                if ('ID=arch' or 'ID_LIKE=arch') in conteudo:
                    versao = "arch"
                    resposta = input('Você está usando um sistema baseado em Arch Linux, e parece que não tem Pywikibot instalado (O que é necessario).\nGostaria de instalar? (S/n)\n: ')
                    paru = False
                    yay = False
                    if resposta == '' or resposta == 'S' or resposta == 's':
                        # Checando se tem helpers
                        for i in range(2):
                            match i:
                                case 0:
                                    try:
                                        
                                        aur_h = os.system("yay --version > /dev/null 2>&1")
                                        yay = True
                                        
                                    except FileNotFoundError:
                                        print("Sem Yay")

                                case 1:
                                    try:
                                        
                                        aur_h = os.system("paru --version > /dev/null 2>&1")
                                        paru = True
                                        
                                    except FileNotFoundError:
                                        print("Sem Paru")

                        if yay and paru:
                            aur_resposta = input("Você tem o Yay e o Paru, qual gostaria de usar para baixar o Pywikibot? \n[1] Yay\n[2] Paru\n: ")
                            if aur_resposta == 1:
                                os.system("yay -S --noconfirm pywikibot")
                            elif aur_resposta == 2:
                                os.system("paru -S --noconfirm pywikibot")

                        elif yay and not paru:
                            print("Instalando a biblioteca pywikibot pelo Yay!")
                            os.system("yay -S --noconfirm pywikibot")

                        elif not yay and paru:
                            print("Instalando a biblioteca pywikibot pelo Paru!")
                            os.system("paru -S --noconfirm pywikibot")

                        elif not yay and not paru:
                            aur_resposta= input("Você não tem nenhum helper do Arch,\nPrefere Yay ou Paru?\n[1] Yay\n[2] Paru\n: ")
                            if aur_resposta == 1:
                                os.system("sudo pacman -S --needed git base-devel && git clone https://aur.archlinux.org/yay.git && cd yay && makepkg -si")
                                os.system("yay -S --noconfirm pywikibot")
                            elif aur_resposta == 2:
                                os.system("sudo pacman -S --needed git base-devel && git clone https://aur.archlinux.org/paru.git && cd paru && makepkg -si")
                                os.system("paru -S --noconfirm pywikibot")

                else:
                    os.system("pip install pywikibot")
        
