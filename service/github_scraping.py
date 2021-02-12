from columnar import columnar
from bs4 import BeautifulSoup
import requests
import re


class GithubScraping:
    def __init__(self, repositorio):
        self.__repositorio = repositorio
        self.arquivos = {}
        self.__checar_branch()

    def __checar_branch(self):
        conteudo = requests.get(f"https://github.com/{self.__repositorio}/branches")
        pagina = BeautifulSoup(conteudo.content, 'html.parser')
        branches = pagina.find("a", class_='branch-name css-truncate-target v-align-baseline width-fit mr-2 Details-content--shown')
        self.__url_file = f"/blob/{branches.get_text()}/"
        self.__url_dir = f"/tree/{branches.get_text()}"

    def __converter_tamanho(self, tamanho_atual, medida):
        if "MB" in medida:
            tamanho_atual = (tamanho_atual * 1024) * 1024
        elif "KB" in medida:
            tamanho_atual = (tamanho_atual * 1024)
        elif "es" in medida:
            pass
        else:
            tamanho_atual = 0
        return tamanho_atual

    def __extrair_informacoes(self, url, nome_arquivo):
        print("Buscando arquivo: ", nome_arquivo)
        dir = url.split(self.__url_file)[-1] + "/" + nome_arquivo

        conteudo = requests.get(url + "/" + nome_arquivo)
        pagina = BeautifulSoup(conteudo.content, 'html.parser')

        linhas = pagina.find_all("div", class_="text-mono f6 flex-auto pr-3 flex-order-2 flex-md-order-1 mt-2 mt-md-0")

        info = re.findall("(\d+\.\d+|\d+)", linhas[0].get_text())
        medida_tamanho = re.findall("(.{2})\s*$", linhas[0].get_text())

        linhas = info[0] if len(info) == 3 else 0
        tamanho = self.__converter_tamanho(round(float(info[-1]), 3), medida_tamanho[0])

        self.__escrever_txt(dir + " ({0}) linhas".format(linhas))

        ext = nome_arquivo.split(".")
        ext = "outros" if ext[0] == "" or len(ext) < 2 else ext[-1]

        self.__count_arquivos(ext, linhas, tamanho)

    def __count_arquivos(self, key, linhas, tamanho):
        try:
            self.arquivos.update(
                {
                    key:
                        {
                            'tamanho': float(self.arquivos[key]['tamanho']) + float(tamanho),
                            'linhas': int(self.arquivos[key]['linhas']) + int(linhas)
                        }
                }
            )
        except KeyError:
            self.arquivos.update(
                {
                    key:
                        {
                            'tamanho': tamanho,
                            'linhas': linhas
                        }
                }
            )

    def __escrever_txt(self, string):
        with open("repositorios/" + self.__repositorio.replace("/", "_") + ".txt", 'a') as arquivo:
            arquivo.write("\n" + string)

    def escrever_tabela(self):
        total_tamanho = 0
        total_linhas = 0
        lista = []
        for i in self.arquivos:
            lista.append([i, self.arquivos[i]['linhas'], self.arquivos[i]['tamanho']])
            total_tamanho += float(self.arquivos[i]['tamanho'])
            total_linhas += int(self.arquivos[i]['linhas'])

        headers = ['Extensão', 'Linhas', 'Bytes']
        table = ""
        lista_completa = []
        for i in lista:
            linhas = (int(i[1]) * 100) / total_linhas
            tamanho = (float(i[2]) * 100) / total_tamanho

            linhas = str(i[1]) + f" ({linhas:.2f} %)"
            tamanho = str(i[2]) + f" ({tamanho:.2f} %)"
            lista_completa.append(
                [
                    i[0],
                    linhas,
                    tamanho,
                 ]
            )
        try:
            table = columnar(lista_completa, headers, no_borders=True)
        except IndexError:
            pass
        self.__escrever_txt(table)

    def iniciar_extracao(self, url_repo):
        request = requests.get(url_repo)
        soup = BeautifulSoup(request.content, 'html.parser')

        table = soup.find_all("div", class_="Box-row Box-row--focus-gray py-2 d-flex position-relative js-navigation-item")

        for i in table:
            nome = i.find_all("a")[0]
            div_arquivos = i.find_all("div", class_="mr-3 flex-shrink-0")

            if "Directory" in str(div_arquivos[0]):
                print("Varrendo diretorio: ", nome.get_text())
                url_repo = request.url
                if self.__url_dir not in url_repo:
                    url_repo = url_repo + self.__url_dir

                url_repo = url_repo + "/" + nome.get_text()
                self.iniciar_extracao(url_repo)
            elif "File" in str(div_arquivos[0]):
                if self.__url_dir in request.url:
                    url_file = request.url.replace(self.__url_dir, self.__url_file)
                else:
                    url_file = request.url + self.__url_file
                self.__extrair_informacoes(url_file, nome.get_text())
