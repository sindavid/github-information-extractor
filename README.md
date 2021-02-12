# github-scraping

##O que é ?
Github Scraping é um projeto desenvolvido para um teste, cujo objetivo é executar um scraping de qualquer repositório que for inserido em um determinado arquivo na raiz do projeto.

Ao executar será criado um diretório `repositorios/` com arquivos `.txt` com o nome do repositório `owner_repository.txt`
Nesse arquivo encontra-se o nome do repositorio, toda estrutura de `pastas/arquivos`do projeto. 
Ao final do arquivo existe uma tabela onde encontra-se todas as extensões dos arquivos inseridos no projeto, quantidade linhas que eles possuem no total e seu tamanho em bytes.

## Como usar?

Para rodar o script é necessário adicionar um arquivo (`repositories.txt`) com uma lista de repositórios a serem analisados.
Após inserir o arquivo basta executar `python app.py`

### Dependencias
    > Python 3.8
    > requests
    > beautifulsoup4
    > columnar

### Instalar dependências Python
Para instalar todas as dependências basta executar `pip install -r requeriments.txt`