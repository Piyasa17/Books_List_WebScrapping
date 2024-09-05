import requests
from bs4 import BeautifulSoup
import pandas as pd
import re

link = "https://books.toscrape.com/"

title = ["Book Name", "Price", "Genre", "Rating", "URL"]
df = pd.DataFrame(columns=title)

for i in range(1,21):
    url = link + "catalogue/page-" + str(i) + ".html"
    r = requests.get(url)
    soup = BeautifulSoup(r.text, 'lxml')
    print(url)

    link_list = soup.find_all("h3")
    href_list = []
    for x in link_list:
        a_tag = x.find("a")
        href_list.append(a_tag.get("href"))
    #print(href_list)

    for y in href_list:
        book_link = "https://books.toscrape.com/catalogue/"+y
        r1 = requests.get(link)
        soup1 = BeautifulSoup(r1.text, 'lxml')

        row = []
        name = soup1.find("h1").string
        price = soup1.find("p", class_="price_color").string

        list_tags = soup1.find_all("li")
        genre = list_tags[2].text

        star = soup1.find("p", class_ = re.compile("star-rating"))
        attribute = star['class']

        row.append(name)
        row.append(price)
        row.append(genre)
        row.append(attribute[1]+" Stars")
        row.append(book_link)

        l = len(df)
        df.loc[l] = row

# print(df)
df.to_csv("Books.csv")
