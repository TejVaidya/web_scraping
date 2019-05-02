import requests

from bs4 import BeautifulSoup
from helper import get_db_connection
from hnews.configurations import *

db = get_db_connection()
coll = "urls"
store = "stored"
links = []
image_src_list=[]

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
    src_url=image["src"]
    image_src_list.append(src_url)
    return(src_url)

selector = 'h3 > a'
found=soup.select(selector)
for x in found:
    link=x.get('href')
    links.append(link)
    print("Url :" +link)
    print("Title : " +x.text)
    desc=get_desc(link)
    img_src=get_img(link)
    print(desc)
    one={"title" : (x.text) , "url" : link , "Description" : desc, "Imagesource" : img_src}
    db[store].insert_one(one)
