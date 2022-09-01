from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
import concurrent.futures



jsfileNewTaipei = open("stationwithbusNewTaipei.json", 'r', encoding='UTF-8')
jswordNewTaipei = jsfileNewTaipei.read()
j=[]
j1= json.loads(jswordNewTaipei)
geohash = []
for i in j1:
    if(i['StationPosition']['GeoHash'] not in geohash):
        j.append(i)
        geohash.append(i['StationPosition']['GeoHash'])
    else:
        print(i["StationPosition"]["GeoHash"])
        geolists = i["Stops"]
        for k in j:
            if(k['StationPosition']['GeoHash']==i['StationPosition']['GeoHash']):
                k["Stops"]+=geolists
                break

jsfileTaipei = open("stationwithbusTaipei.json", 'r', encoding='UTF-8')
jswordTaipei = jsfileTaipei.read()
j2 = json.loads(jswordTaipei)
for i in j2:
    if(i['StationPosition']['GeoHash'] not in geohash):
        j.append(i)
        geohash.append(i['StationPosition']['GeoHash'])
    else:
        print(i["StationPosition"]["GeoHash"])
        geolists = i["Stops"]
        for k in j:
            if(k['StationPosition']['GeoHash']==i['StationPosition']['GeoHash']):
                k["Stops"]+=geolists
                break

#m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=11, control_scale=True)
#outfile = open("stationlist.txt", "w", encoding='UTF-8')

fs=open("test.txt", 'w', encoding='utf-8')
for i in j:
    fs.write(i["StationName"]["Zh_tw"]+'\n')
    for k in i["Stops"]:
        fs.write(k["RouteName"]["Zh_tw"]+'\n')