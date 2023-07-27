import requests
from bs4 import BeautifulSoup

async def get_article(item_soup):
    link = item_soup.find("link")
    url = link.text
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')
    image = item_soup.find("media:content").get("url")
    tags = ", ".join(set([f'#{k.text.replace(" ", "_").capitalize()}' for k in item_soup.find_all("category")]))
    category = soup.find("div", {"class": "at-category"}).text
    creator = item_soup.find("dc:creator").text
    pub_date = item_soup.find("pubDate").text.replace("+0000", "UTC")
    headline = soup.find("div", {"class": "at-headline"}).text
    subheadline = soup.find("div", {"class": "at-subheadline"}).text
    text_data = soup.find("div", {"data-submodule-name":"composer-content"}).find("div").text

    data = {
        "image": image,
        "headline": headline,
        "subheadline": subheadline,
        "creator": creator,
        "category": category,
        "pub_date": pub_date,
        "text_data": text_data,
        "tags": tags,
        "url": url
    }
    
    return data