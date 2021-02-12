from service.github_scraping import GithubScraping
import os

try:
    if "repositorios" not in os.listdir(os.getcwd()):
        os.makedirs("repositorios")
    with open('repositories.txt', 'r') as arquivo:
        for repositorio in arquivo:
            repositorio = repositorio.strip("\n")
            print("Iniciando processo para o repositório :", repositorio)
            with open("repositorios/" + repositorio.replace("/", "_") + ".txt", 'a+') as arquivo:
                arquivo.write(repositorio + "\n")

            git = GithubScraping(repositorio)
            url_base = "https://github.com/"

            git.iniciar_extracao(url_base + repositorio.strip("\n"))
            git.escrever_tabela()
            print("Repositório ", repositorio, "finalizado.\n")
except FileNotFoundError:
    print("Arquivo repositories.txt não foi encontrado")
