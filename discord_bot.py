import discord
import os
import requests
import json
import rsa
from dotenv import load_dotenv
import config
import matplotlib.pyplot as plt
import numpy as np


intents = discord.Intents.all()
client = discord.Client(intents=intents)
token = config.TOKEN

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def all_currency_price():
    response = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
    json_data = json.loads(response.text)
    currency1 = json_data["USDBRL"]['name'] + " -- Máxima: " + json_data["USDBRL"]['high'] + " -- Mínima: " + json_data["USDBRL"]['low'] 
    currency2 = json_data["EURBRL"]['name'] + " -- Máxima: " + json_data["EURBRL"]['high'] + " -- Mínima: " + json_data["EURBRL"]['low'] 
    currency3 = json_data["BTCBRL"]['name'] + " -- Máxima: " + (json_data["BTCBRL"]['high'] )+ " -- Mínima: " + (json_data["BTCBRL"]['low']) 
    currencies = f'{currency1}  {os.linesep}{currency2}  {os.linesep}{currency3}'
    return(currencies)

def last_month_usd_prices():
    response = requests.get("https://economia.awesomeapi.com.br/json/daily/USD-BRL/30")
    json_data = json.loads(response.text)   
    currency_high = np.empty(30)
    currency_low = np.empty(30)
    for i in range(0,30):
        currency_high[i] = json_data[i]['high']
    for i in range(0,30):
        currency_low[i] = json_data[i]['low']

    range_days = np.empty(30)
    for i in range (0,30):
        range_days[i] = (-i)

    plt.clf()
    plt.plot(range_days,currency_high, label="máxima")
    plt.plot(range_days,currency_low, label="mínima")
    plt.title('USD-BRL price - Last 30 days')
    plt.xlabel('Last 30 days')
    plt.ylabel('USD-BRL Price')
    filename =  "test.png"
    plt.savefig(filename)
    image = discord.File(filename)
    return image

def last_month_eur_prices():
    response = requests.get("https://economia.awesomeapi.com.br/json/daily/EUR-BRL/30")
    json_data = json.loads(response.text)   
    currency_high = np.empty(30)
    currency_low = np.empty(30)
    for i in range(0,30):
        currency_high[i] = json_data[i]['high']
    for i in range(0,30):
        currency_low[i] = json_data[i]['low']
 
    range_days = np.empty(30)
    for i in range (0,30):
        range_days[i] = (-i)
        
    plt.clf()
    plt.plot(range_days,currency_high, label = "máxima")
    plt.plot(range_days,currency_low, label = "mínima")
    plt.title('EUR-BRL price - Last 30 days')
    plt.xlabel('Last 30 days')
    plt.ylabel('EUR-BRL Price')    
    plt.legend()    
    filename =  "test.png"
    plt.savefig(filename)
    image = discord.File(filename)
    return image

def convert_amount(message):
    response = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL")
    json_data = json.loads(response.text)
    price_usd = json_data["USDBRL"]['bid']
    response = requests.get("https://economia.awesomeapi.com.br/last/EUR-BRL")
    json_data = json.loads(response.text)
    price_eur = json_data["EURBRL"]['bid']
    messageSplit = message.content.split(" ")
    if len(messageSplit) == 3:
        if messageSplit[1] == "USD":
            try:
                converted_amount = (float(price_usd) * float(messageSplit[2]))   
                return ("R$"f'{converted_amount}')
            except:
                return ("Comando inválido, tente $ajuda")
        elif messageSplit[1] == "EUR":
            try:
                converted_amount = (float(price_eur) * float(messageSplit[2]))
                return ("R$"f'{converted_amount}')
            except:
                return ("Comando inválido, tente $ajuda")
        else:
            return ("Comando inválido, tente $ajuda")
    else:
        return ("Comando inválido, tente $ajuda")


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$ajuda'):
        await message.author.send(f'{message.author.name}, Confira aqui os nossos comandos: {os.linesep}1- Para verificar a cotação diária do Dollar, Euro e Bitcoin, utilizar o comando: $currencies . {os.linesep}2- Para verificar o histórico dos últimos 30 dias, temos comandos para o dollar e o euro, sendo eles: $usd-brl-30days   e  $eur-brl-30days   .{os.linesep}3- Para realizar uma conversão para reais, temos o comando $convert USD valor e $convert EUR valor, exemplo: $convert USD 100  .  {os.linesep}4- E por fim, um comando para quando queira alguma frase famosa aleatória, para descontrair, utilieze: $quote   .')
   
    if message.content.startswith('$quote'):
        quote = get_quote()
        await message.channel.send(quote)
        
    if message.content.startswith('$currencies'):
        currencies = all_currency_price()
        await message.channel.send(currencies)        

    if message.content.startswith('$usd-brl-30days'):
        currency1 = last_month_usd_prices()
        await message.channel.send(file = currency1)
        
    if message.content.startswith('$eur-brl-30days'):
        currency2 = last_month_eur_prices()
        await message.channel.send(file = currency2)    
           
    if message.content.startswith('$convert'):
        amount = convert_amount(message)
        await message.channel.send(amount)          
        
@client.event
async def on_member_join(member):
    await member.send(
        f'Olá {member.name}, bem vindo ao server! Somos um bot multi funcional, com foco em alguns comandos de cotação das principais moedas internacionais do mercado. Qualquer duvida digite $ajuda .'
    )

client.run(token)
 

