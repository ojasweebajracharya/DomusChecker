from audioop import add
from bs4 import BeautifulSoup
import requests

url = "https://domus.ed.ac.uk/properties/"

result = requests.get(url)

doc = BeautifulSoup(result.text, "html.parser")

addresses = doc.find_all('p', class_='property-address')

postcode = []

for each in addresses:
    postcode.append(str(each.get_text()))

print(postcode[0])


# Get all property names, addresses, bedrooms, postcode and link


# filter only addresses

