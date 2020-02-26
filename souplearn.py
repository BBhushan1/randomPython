from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import ssl

#Url to scrape
myURL = 'http://www.amazon.in/s?crid=3MOCIP633CEQN&i=aps&k=xbox%20360%20console&ref=nb_sb_ss_i_4_11&sprefix=xbox%20360%20co%2Caps%2C262&url=search-alias%3Daps'

#Gangster for SSL Error ;)
gcontext = ssl.SSLContext()
#Fetch the page
page_html = uReq(myURL, context=gcontext).read()
#html parsing
page_soup = soup(page_html, "html.parser")
#grabs search results for URL
containers = page_soup.find_all("div", {"class": "s-result-item"})
for container in containers:
    product_container = container.find_all("span", {"class": "a-text-normal"})
    product_name = product_container[0].text
    price_container =  container.find_all("span", {"class": "a-price-whole"})
    price = price_container[0].text
    print(price_container)