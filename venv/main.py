from bs4 import BeautifulSoup
import requests

url = "https://domus.ed.ac.uk/properties/"

result = requests.get(url)
print(result.text)
