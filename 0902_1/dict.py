from time import sleep
import folium
from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
from folium.plugins import Search
import concurrent.futures
import polyline
import time

import bs4, requests, os

#m = folium.Map(location=[25.046436, 121.517463], zoom_start=11,tiles="Cartodb Positron", max_zoom=25)

import bs4, requests, os
import concurrent.futures
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101\
            Safari/537.36', }


ImagefileNewTaipei = open("ImageNewTaipei.json", 'r', encoding='UTF-8')
ImagewordNewTaipei = ImagefileNewTaipei.read()
j6= json.loads(ImagewordNewTaipei)
ImagefileTaipei = open("ImageTaipei.json", 'r', encoding='UTF-8')
ImagewordTaipei = ImagefileTaipei.read()
j7= json.loads(ImagewordTaipei)
j8=j6+j7
print(len(j8))
imagelist = {}
for i in j8:
    try:
        routeimagelink = i["RouteMapImageUrl"]
        print(routeimagelink)
        html = requests.get(routeimagelink, headers=headers)
        objSoup = bs4.BeautifulSoup(html.text, 'lxml')
        sublink=objSoup.select('img')[0].get('src')
        sublink=sublink[1:]
        finallink = 'https://ebus.gov.taipei' + sublink
        print(finallink)
        imagelist.setdefault(i["RouteName"]["Zh_tw"],i["RouteMapImageUrl"])
    except:
        routeimagelink = i["RouteMapImageUrl"]
        print(routeimagelink)
        html = requests.get(routeimagelink, headers=headers)
        objSoup = bs4.BeautifulSoup(html.text, 'lxml')
        sublink=objSoup.select('img')[0].get('src')
        sublink=sublink[1:]
        finallink = 'https://ebus.gov.taipei' + sublink
        print(finallink)
        imagelist.setdefault(i["RouteName"]["Zh_tw"],i["RouteMapImageUrl"])
print(imagelist)