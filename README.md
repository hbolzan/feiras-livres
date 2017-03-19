# feiras-livres
API REST para manipulção e pesquisa de dados sobre feiras livres de São Paulo

## Apresentação
Esta API foi desenvolvida em Python com Django Framework, sem utilização do REST Framework. O desenvolvimento e os testes foram feitos em um Linux box com Ubuntu 16.10. As instruções a seguir presumem a instalação em um sistema operacional Linux mas devem servir igualmente para instalação em MacOS e outros UNIX'es.

O banco de dados relacional escolhido para este projeto foi SQLite3 devido à facilidade de uso (não exige instalação de servidor). Porém, ele pode facilmente ser substituído por outro banco, já que todo acesso aos dados é feito através do ORM do Django.

## Pré requisitos
* python 2.7
* Sitema de controle de versão git - https://git-scm.com/
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
   $ git clone git@github.com:hbolzan/feiras-livres.git
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

   Foi incluído no projeto um script de linha de comando para importação do CSV publicado pela Prefeitura de São Paulo contendo dados das feiras livres. No respositório, está incluído o arquivo `DEINFO_AB_FEIRASLIVRES_2014.csv`. A importação não é incremental, ou seja, os dados existentes no banco são apagados antes de iniciar uma nova importação.
   ```
   $ ./manage.py importar_feiras feiras_livres/csv/DEINFO_AB_FEIRASLIVRES_2014.csv
   ```

7. Rode o servidor de desenvolvimento do Django
   ```
   $ ./manage.py runserver
   ```
   A porta default é 8000. Se quiser rodar o servidor em outra porta, especifique nos parâmetros do comando. Para utilizar a porta 7878, por exemplo:
   ```
   $ ./manage.py runserver 0.0.0.0:7878
   ```

## Testes

### Execução

### Relatório de cobertura

## Recursos

