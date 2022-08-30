from lib2to3.pytree import convert
import bs4, requests, os, json, folium
import concurrent.futures
'''
headers = { 'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64)\
            AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101\
            Safari/537.36', }
url = 'https://ptx.transportdata.tw/MOTC/v2/Bus/Stop/City/NewTaipei?%24top=21000&%24format=JSON'
html = requests.get(url, headers=headers)
objSoup = bs4.BeautifulSoup(html.text, 'lxml')
j= json.loads(objSoup.text)
m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=14)
for i in j:
    longtitude = i['StopPosition']['PositionLon']
    latitude = i['StopPosition']['PositionLat']
    stopname = i['StopName']['Zh_tw']
    folium.CircleMarker(
        location=[latitude, longtitude],
        radius=3,
        popup=stopname,
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(m)

m.save('myMap.html')
'''

jsfileNewTaipei = open("response_1661839141867.json", 'r', encoding='UTF-8')
jswordNewTaipei = jsfileNewTaipei.read()
j=[]
j1= json.loads(jswordNewTaipei)
geohash = []
for i in j1:
    if(i['StopPosition']['GeoHash'] not in geohash):
        j.append(i)
        geohash.append(i['StopPosition']['GeoHash'])
jsfileTaipei = open("response_1661839582841.json", 'r', encoding='UTF-8')
jswordTaipei = jsfileTaipei.read()
j2 = json.loads(jswordTaipei)
for i in j2:
    if(i['StopPosition']['GeoHash'] not in geohash):
        j.append(i)
        geohash.append(i['StopPosition']['GeoHash'])

m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=14)
outfile = open("stationlist.txt", "w", encoding='UTF-8')
for i in j:
    longtitude = i['StopPosition']['PositionLon']
    latitude = i['StopPosition']['PositionLat']
    stopname = i['StopName']['Zh_tw']
    outfile.write(stopname+' '+str(latitude)+str(longtitude)+'\n')
    folium.CircleMarker(
        location=[latitude, longtitude],
        radius=3,
        popup=stopname,
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(m)

m.save('myMap.html')