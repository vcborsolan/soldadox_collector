![Logo do projeto](https://github.com/vcborsolan/soldadox/blob/master/logo.png)

## O que é este projeto?


Soldadox colector é um microserviço dedicado para coleta de dados provindos da OLX e os armazena visando disponibilizar dados para analise e processamento do projeto soldadox , o mesmo ainda esta em fase de desenvolvimento / testes , caso tenha interesse fique a vontade para abrir um fork ou contribuir com o projeto.


## O que o projeto usa? 
Neste Projeto é usado Sentry como gestor de logs , beautifilsoup4 para os crawlers , flask como frameworkweb , docker para deploy.

## Como instalar?

1. Clonar o projeto :

    $ https://github.com/vcborsolan/soldadox.git

2. O projeto todo esta dockerizado , para tanto então temos de buildar a imagem com:

    $ docker build -t 'image_name' .

3. Rodar o container com:

    $ docker run -p 5001:5001 test_flask:latest

## Features:

1. /cadastrar {POST} visa caso seja necessario ou de interesse buildar um novo db , ser um path para migrar todos os dados iniciais de estados , municipios e regioes por ddd ; que incluisve esta incompleto até então. Essa 'migration' em json esta no projeto como seed.json.

2. /show {GET} , para eventuais testes se foi migrado o passo anterior , futuramente será retirado.

3. /api/ads {POST} pode receber por parametros em json :ddd , :region , :state , :search , :nofp , :lastAd.
Para que fique mais claro segue exemplo de requisão:

{
    "state": "SP" ,
	"ddd": "DDD 11 - São Paulo e região" ,
	"region": "Centro" ,
	"search": "Guitarra",
	"nofp": 1,
	"lastAd": "751261839"
}

Sendo obrigatorio apenas :search , cujo corresponde ao alvo da pesquisa na olx , os demais por default :state , :ddd e :region se der erro vão direcionar a url da olx brasil . :nofp é a quantidade de paginas que se quer buscar , por default é 1. :lastAd tem como alvo mandar buscar até achar determinado anuncio , importante aqui ressaltar que os anuncionar NÃO são necessariamentes listados sequencialmente , sendo assim , podendo ser perdido dados , recomendo que use esta variavel apenas em casos especificos. Estudo aqui receber um array com 1000 Para aumentar a credibilidade assim como tem sido feito em '/cron'.

4. /api/ad/<adcode> {GET} , recebe por parametro :adcode , visa verificar no bd se há o anuncio respectivo e caso não haja o busque para salvar no bd e retornar ele em json.

5. /cron {GET} , tem o objetivo tem cadastrar o cron para o tempo desejado e realizar a pesquisa.
Por default ele esta realizando a pesquisa em marilia/sp , enviando os ultimo mil anuncios cadastrados no bd e buscando no maximo as ultimas 10 paginas da OLX .

## Autor :
 
**Victor Cesar Barbosa Orsolan**: @vcborsolan (https://github.com/vcborsolan)
Caso precise de ajuda entre em contato pelo email vorsolan@hotmail.com