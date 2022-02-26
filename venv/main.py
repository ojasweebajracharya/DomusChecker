from audioop import add
from bs4 import BeautifulSoup
import requests

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

# for i in range(len())

# print(links[0]['href']) # example of how to get the linkkk

postcode = []

for each in addresses:
    postcode.append(str(each.get_text()))


for i in range(len(addresses)):
    properties.append([streetnames[i].next, postcode[i], links[i]['href']])

print(properties[0])


# Get all property names, addresses, bedrooms, postcode and link


# filter only addresses

