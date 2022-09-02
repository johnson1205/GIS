import folium
from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
from folium.plugins import Search
import concurrent.futures
import polyline


#m = folium.Map(location=[25.046436, 121.517463], zoom_start=11,tiles="Cartodb Positron", max_zoom=25)

ImagefileNewTaipei = open("ImageNewTaipei.json", 'r', encoding='UTF-8')
ImagewordNewTaipei = ImagefileNewTaipei.read()
j6= json.loads(ImagewordNewTaipei)
ImagefileTaipei = open("ImageTaipei.json", 'r', encoding='UTF-8')
ImagewordTaipei = ImagefileTaipei.read()
j7= json.loads(ImagewordTaipei)
j8=j6+j7

imagelist = {}
for i in j8:
    imagelist.setdefault(i["RouteName"]["Zh_tw"],i["RouteMapImageUrl"])
