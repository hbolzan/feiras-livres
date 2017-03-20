# feiras-livres
API REST para manipulção e pesquisa de dados sobre feiras livres de São Paulo

## Apresentação
Esta API foi desenvolvida em Python com Django Framework, sem utilização do REST Framework. O desenvolvimento e os testes foram feitos em um Linux box com Ubuntu 16.10. As instruções a seguir presumem a instalação em um sistema operacional Linux mas devem servir igualmente para instalação em MacOS e outros UNIX'es.

O banco de dados relacional escolhido para este projeto foi o SQLite3 devido à facilidade de uso (não exige instalação de servidor). Porém, ele pode facilmente ser substituído por outro banco, já que o acesso aos dados é feito através do ORM do Django.

## Pré requisitos
* python 2.7
* Sistema de controle de versão git - https://git-scm.com/
* Gerenciador de pacotes pip - https://pip.pypa.io/en/stable/
* Virtualenv - https://virtualenv.pypa.io/en/stable/
* Uma ferramenta para fazer requests REST para testar a API como, por exemplo, o Postman plugin para o Google Chrome - https://chrome.google.com/webstore/detail/postman/fhbjgbiflinjbdggehcddcbncdddomop
  

## Instalação
1. Abra um terminal e escolha a sua pasta de projetos. Para este exemplo será usada uma pasta chamada `projetos` na home do usuário.
   ```
   $ cd ~/projetos
   ```

2. Clone o projeto no github e mude para o diretório do projeto
   ```
   $ git clone https://github.com/hbolzan/feiras-livres.git
   $ cd feiras-livres
   ```

3. Crie e ative um ambiente virtual para instalação dos pacotes
   ```
   $ virtualenv ~/.virtualenvs/feiras
   $ source ~/.virtualenvs/feiras/bin/activate
   ```

4. Instale os pacotes requeridos pelo sistema
   ```
   $ pip install -r requirements.txt
   ```

5. Inicie o schema de dados
   ```
   $ ./manage.py migrate
   ```

6. Importação do CSV

   Foi incluído no projeto um script de linha de comando para importação do arquivo CSV que contém os dados das feiras livres. No respositório, está incluído o arquivo `DEINFO_AB_FEIRASLIVRES_2014.csv`. A importação não é incremental, ou seja, os dados existentes no banco são apagados antes de iniciar uma nova importação.
   ```
   $ ./manage.py importar_feiras feiras_livres/csv/DEINFO_AB_FEIRASLIVRES_2014.csv
   ```

7. Rode o servidor de desenvolvimento do Django
   ```
   $ ./manage.py runserver
   ```
   A porta padrão do servidor de desenvolvimento é 8000. Se quiser rodar o servidor em outra porta, especifique nos parâmetros do comando. Para utilizar a porta 7878, por exemplo:
   ```
   $ ./manage.py runserver 0.0.0.0:7878
   ```
8. No navegador, aponte para o endereço `http://localhost:8000/api/v1.0/feiras/` ou, se tiver escolhido outra porta, substitua o `8000` na url pelo número da porta escohida. Para fazer requisições com métodos diferentes de GET, será necessário utilizar um cliente de API REST como o Postman.

## Testes
A aplicação inclui três test cases que cobrem as principais funções dos endpoints.

### Execução
Para rodar os testes, digite na linha de comando:
   ```
   $ ./manage.py test
   ```

### Relatório de cobertura
Para gerar o relatório de cobertura de testes, utilize o módulo `coverage` que já está incluído nos requirements do projeto.
   ```
   $ coverage run --source '.'  manage.py test
   $ coverage report
   ```


## Recursos
### /feiras/
   ```
   /api/v1.0/feiras/
   ```
#### Métodos   
* __GET__: retorna a tabela completa de feiras
* __POST__: adiciona uma feira

### /feiras/:id/
   ```
   /api/v1.0/feiras/:id/
   ```
#### Métodos   
* __GET__: retorna a feira identificada por :id
* __DELETE__: exclui a feira identificada por :id
* __PATCH__: altera dados da feira identificada por :id
* __PUT__: altera dados da feira identificada por :id 

### /feiras/busca/
Pesquisa na tabela de feiras. Pesquisas podem ser feitas pelos campos `distrito`, `regiao_5`, `nome` e `bairro`.
   ```
   /api/v1.0/feiras/busca/?parametros
   ```
#### Métodos   
* __GET__: retorna os dados filtrados conforme parâmetros da URL.


## Mais informações
Detalhes adicionais, informações sobre os recursos e exemplos de uso: https://github.com/hbolzan/feiras-livres/wiki
