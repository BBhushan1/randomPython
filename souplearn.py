from bs4 import BeautifulSoup as soup
from urllib.request import urlopen as uReq
import ssl

# Url to scrape
myURL = 'https://www.mohfw.gov.in/'

# Gangster for SSL Error ;)
gcontext = ssl.SSLContext()
# Fetch the page
page_html = uReq(myURL, context=gcontext).read()
# html parsing
page_soup = soup(page_html, "html.parser")
# grabs search results for URL
# containers = page_soup.find_all("div", {"class": "s-result-item"})
# for container in containers:
#     product_container = container.find_all("span", {"class": "a-text-normal"})
#     product_name = product_container[0].text
#     price_container = container.find_all("span", {"class": "a-price-whole"})
#     price = price_container[0].text
#     print(price_container)
#print(page_soup)
# page_spans = page_soup.find_all("span",{"class": "icount"})
# print(page_spans)

page_divs = page_soup.find_all("div",{"class": "iblock"})
for info in page_divs:
    info_label_array = info.find_all("div",{"class": "info_label"})
    info_label= info_label_array[0].text
    count_label_array = info.find_all("span",{"class": "icount"})
    count_label = count_label_array[0].text
    print(info_label + ': '+ count_label)