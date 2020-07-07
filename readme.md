# Como rodar o projeto


```sh
pipenv install requests beautifulsoup4 flask flask-sqlalchemy flask-migrate flask-marshmallow marshmallow-sqlalchemy
export FLASK_APP=App
export FLASK_ENV=development
```
Neste Projeto é usado Sentry como gestor de logs , postman para testes e documentação.





<!-- Planejamento:

    O que a API faz: coleta de dados da olx.
        Pode ser consultado:
            >> Todos os anuncios ativos apenas com base numa 'frase'
            >> Melhorar a consulta acima com filtros de "Estado" , "DDD" , "Região" , "Qtd de paginas max" , apenas mais recentes que determinado código (Para uso continuo).
            >> Se o anuncio esta ativo , foi editado ou expirou baseado como parametro a url.

    O que a API não faz:
        A api não retorna dados de contato cep e bairro do anunciante. 


    Onde parei:

    as apis estao funcionais , precisa agora criar o agendador de busca e o front end
 -->