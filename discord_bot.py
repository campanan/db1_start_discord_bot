import os
import discord
import os
import requests
import json
import rsa
from dotenv import load_dotenv
import config

intents = discord.Intents.all()
client = discord.Client(intents=intents)

token = config.TOKEN;

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)

def moedas_price():
    response = requests.get("https://economia.awesomeapi.com.br/last/USD-BRL,EUR-BRL,BTC-BRL")
    json_data = json.loads(response.text)
    moeda1 = json_data["USDBRL"]['name'] + " -- Máxima: " + json_data["USDBRL"]['high'] + " -- Mínima: " + json_data["USDBRL"]['low'] 
    moeda2 = json_data["EURBRL"]['name'] + " -- Máxima: " + json_data["EURBRL"]['high'] + " -- Mínima: " + json_data["EURBRL"]['low'] 
    moeda3 = json_data["BTCBRL"]['name'] + " -- Máxima: " + (json_data["BTCBRL"]['high'] )+ " -- Mínima: " + (json_data["BTCBRL"]['low']) 
    moedas = f'{moeda1}  {os.linesep}{moeda2}  {os.linesep}{moeda3}'
    return(moedas)

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
        
    if message.content.startswith('$moedas'):
        moedas = moedas_price()
        await message.channel.send(moedas)
        
@client.event
async def on_member_join(member):
    await member.send(
        f'Olá {member.name}, bem vindo ao server!'
    )


client.run(token)
 

