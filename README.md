# db1_start_discord_bot

Esse projeto é um bot de discord, com fim educativo, um projeto final da formação DB1 Start.

Nesse projeto utilizamos algumas API's grátis, como a AwesomeAPI e ZenQuotes.

#Desenvolvimento

O desenvolvimento fio feito em Python, utilizando o pacote discod.py. Também foram utilizados nesse projeto matplotlib, numpy e outros pacotes.

#Instalação do BOT

Hoje a instalação ainda se da através da IDE ou terminal. Onde primeiro é necessário instalar as libs utilizadas.

Para isso, primeiro clonamos o repositório, e instalamos os pacotes utilizados, através do requirements.txt gerado por nosso virtualenv. 
```
$ pip install -r path/to/requirements.txt
```

No repositório, criar o arquivo config.py onde deverá ser incluido o TOKEN do seu bot discord. com o formato:

```
TOKEN='digite_aqui_o_seu_token'
```

O seu bot deve estar com todas as permissões de intents liberadas.

Após isso, executar o arquivo discord_bot.py por sua IDE ou terminal.