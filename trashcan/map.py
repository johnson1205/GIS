from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
import concurrent.futures



jsfileNewTaipei = open("trash.json", 'r', encoding='UTF-8')
jswordNewTaipei = jsfileNewTaipei.read()
j=[]
j1= json.loads(jswordNewTaipei)
for i in j1:
    j.append(i)

m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=11, control_scale=True)


for i in j:
    longtitude = i["經度"]
    latitude = i["緯度"]
    try:
        folium.Circle(
            location=[latitude, longtitude],
            radius=3,
            color='#3186cc',
            fill=True,
            fill_color='#3186cc'
        ).add_to(m)
    except:
        continue

m.save('myMap.html')