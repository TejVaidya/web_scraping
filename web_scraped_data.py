import requests

from bs4 import BeautifulSoup
from helper import get_db_connection
from hnews.configurations import *

db = get_db_connection()
coll = "urls"
store = "stored"
links = []

source = requests.get("https://medium.com/topic/editors-picks").text
soup = BeautifulSoup(source, "lxml")

def get_desc(link):
    source=requests.get(link).text
    soup = BeautifulSoup(source, "lxml")
    try:
        description = soup.find("h2")
        txt=description.text
        return(txt)
    except AttributeError:
        desc = soup.find("p")
        txt=desc.text
        return(txt)
    
def get_img(src):
    source=requests.get(src).text
    soup=BeautifulSoup(source,"lxml")
    image=soup.find("img")
    sour=image["src"]
    return(sour)

selector = 'h3 > a'
found=soup.select(selector)
for x in found:
    link=x.get('href')
    links.append(link)
    print("Url :" +link)
    print("Title : " +x.text)
    desc=get_desc(link)
    print(desc)
    one={"title" : (x.text) , "url" : link , "Description" : desc}
    db[store].insert_one(one)
