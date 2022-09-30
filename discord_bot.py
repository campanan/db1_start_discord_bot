import os
import discord
import os
import requests
import json
import rsa
from dotenv import load_dotenv
import config
import matplotlib.pyplot as plt
import numpy

intents = discord.Intents.all()
client = discord.Client(intents=intents)

token = config.TOKEN;

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
    currency = numpy.empty(30)
    for i in range(0,30):
        currency[i] = json_data[i]['high']
    
    formated_currency = [ '%.2f' % elem for elem in currency]

    range_days = numpy.empty(30)
    for i in range (0,30):
        range_days[i] = (-i)

    plt.title('USD-BRL price - Last 30 days')
    plt.xlabel('Last 30 days')
    plt.ylabel('USD-BRL Price')    
    plt.plot(range_days,currency)
    plt.xticks([])
    filename =  "test.png"
    plt.savefig(filename)
    image = discord.File(filename)
    return image

def last_month_eur_prices():
    response = requests.get("https://economia.awesomeapi.com.br/json/daily/EUR-BRL/30")
    json_data = json.loads(response.text)   
    currency = numpy.empty(30)
    for i in range(0,30):
        currency[i] = json_data[i]['high']
    
    formated_currency = [ '%.2f' % elem for elem in currency]

    range_days = numpy.empty(30)
    for i in range (0,30):
        range_days[i] = (-i)

    plt.title('EUR-BRL price - Last 30 days')
    plt.xlabel('Last 30 days')
    plt.ylabel('EUR-BRL Price')    
    plt.xticks([])
    plt.plot(range_days,currency)
    filename =  "test.png"
    plt.savefig(filename)
    image = discord.File(filename)
    return image


@client.event
async def on_ready():
    print(f'We have logged in as {client.user}')

@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$regras'):
        await message.channel.send(f'{message.author.name} as regras do servidor são: {os.linesep}1- Respeitar a todos. {os.linesep}2- Não utilizar linguajar inadequado.')
   
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


            
        
@client.event
async def on_member_join(member):
    await member.send(
        f'Olá {member.name}, bem vindo ao server!'
    )


    


client.run(token)
 

