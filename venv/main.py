from bs4 import BeautifulSoup
import requests
import discord
import os

client = discord.Client()
@client.event
async  def on_ready():
    print("WE have logged in as {0.user".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")

client.run(os.getenv('TOKEN'))

def scrapeDomus():
    url = "https://domus.ed.ac.uk/properties/"

    result = requests.get(url)

    properties = []

    doc = BeautifulSoup(result.text, "html.parser")

    streetnames = doc.find_all('h3') # ignore first and last it's just "refine search"

    # cleaning streetnames
    streetnames.pop(0)
    streetnames.pop(len(streetnames) - 1)

    addresses = doc.find_all('p', class_='property-address')
    links = doc.find_all('a', class_='property-title-link')
    prices = doc.find_all('p', class_='property-price')

    postcode = []

    for each in addresses:
        input = str(each.get_text())
        input = " ".join(input.split())
        postcode.append(input[-7:])


    for i in range(len(addresses)):
        properties.append([streetnames[i].next, postcode[i], links[i]['href']])

    return properties

