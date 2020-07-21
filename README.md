# Programa de estágio AIKO - Teste Back-end

Teste Back-end do programa de estágio AIKO.

## Sobre o repositório

Esse repositório contém a implementação do teste Back-end do programa de estágio AIKO. Onde foi desenvolvido um clone da API OlhoVivo. Tal aplicação realiza consultas e inserções de dados de Paradas, Linhas, Veículos e suas respectivas posições. Os arquivos são de scripts que representam as seguintes aplicações em containers:

### API - back-end

Aplicação de consulta e inserção de dados de linhas, paradas e veiculos.

Acesso pela porta 8000

### Postgres

Banco de dados utilizado pela API

## Apresentação da API

Neste [link](https://www.youtube.com/watch?v=YlfStR3-YYs) pode ser encontrada a aprensentação em vídeo da API implementada. No vídeo apresento detalhes de infraestrutura, implementação e utilização.

## Instalação

**1.** Build das imagens do ambiente:

```bash
docker-compose build
```

**2.** Subir containers:

```bash
docker-compose up -d
```

**3.** Verifique se os serviços subiram corretamente:

```bash
docker ps
```

E se os containers estiverem rodando corretamente, você irá visualizar uma saída parecida com:

```bash
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                    NAMES
e4ef66e22cea        aiko_backend        "./wait-for-database…"   2 minutes ago       Up 2 minutes        0.0.0.0:8000->8000/tcp   backend
fd343b14c5ef        postgres            "docker-entrypoint.s…"   2 minutes ago       Up 2 minutes        5432/tcp                 db
```

## Testes

Para verificar se a instalação ocorreu corretamente rode os testes que estão no container backend. Para isso execute o seguinte comando:

```bash
docker exec -it backend python manage.py test
```

Se não houver falhas você obterá uma saída parecida com:

```bash
Creating test database for alias 'default'...
System check identified no issues (0 silenced).
...........................................
----------------------------------------------------------------------
Ran 43 tests in 1.521s

OK
Destroying test database for alias 'default'...
```