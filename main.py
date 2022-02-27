import aiocron
from bs4 import BeautifulSoup
import requests
import discord
import os


client = discord.Client()
# @client.event
# async def on_ready():
#     print("WE have logged in as {0.user".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return
    if message.content.startswith("$hello"):
        await message.channel.send("Hello!")


# @aiocron.crontab('*/10 08-010 * * *')
# async def cornjob():
#     await scrapeDomus()


@aiocron.crontab('58 18 * * *')
async def cornjob():
    await loopPagesDomus()


async def loopPagesDomus():
    # so we've capped the page number at 5 max, too long to try fix it accurately.
    # realistically, it won't go above 5 anyway so I thin we're good.
    domusChannel = client.get_channel(947544149647851610)
    url = "https://domus.ed.ac.uk/properties/#/requested_page=2&sort_order=DESC&sort_by=price&i=1"
    await printScrapeDomusResults(url)

    # for page_num in range(1, 5):
    #     url = "https://domus.ed.ac.uk/properties/#/requested_page=" + str(page_num) + "&sort_order=DESC&sort_by=price&i=1&unique_hash=93733"
    #     await domusChannel.send("page: " + str(page_num))
    #     await domusChannel.send("url: " + url)
    #     await printScrapeDomusResults(url)

    for page_num in range(2, 3):
        url = "https://domus.ed.ac.uk/properties/#/requested_page=" + str(page_num) + "&sort_order=DESC&sort_by=price&i=1&unique_hash=93733"
        await domusChannel.send("page: " + str(page_num))
        await domusChannel.send("url: " + url)
        await printScrapeDomusResults(url)


async def printScrapeDomusResults(url):
    domusChannel = client.get_channel(947544149647851610)

    await domusChannel.send(scrapeDomus(url))


def scrapeDomus(url):
    # url = "https://domus.ed.ac.uk/properties/"

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


client.run(os.getenv('TOKEN'))
