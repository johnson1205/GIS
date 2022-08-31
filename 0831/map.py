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



m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=11, control_scale=True)

#---
def popup_html(i):
    nameMandarin = ""
    try:
        nameMandarin = i['StationName']['Zh_tw']
    except:
        nameMandarin = ""

    nameEnglish = ""
    try:
        nameEnglish=i["Stops"][0]['StopName']['En']
    except:
        nameEnglish=""

    buslist=[]
    for bus in i["Stops"]:
        buslist.append(bus["RouteName"]["Zh_tw"])
    buslist.sort();
    busstr=""
    for buses in buslist:
        busstr+=buses+','
    busstr=busstr[:-1]

    html = """
<!DOCTYPE html>
<html>
<table style="border-collapse: collapse; width: 500px; height: 36px;" border="1">
<tbody>
<tr style="height: 18px;">
<td style="text-align: center;background-color: """+ "#3366ff" +""";"colspan="2" style="width: 150px; height: 18px;">
<h4><span style="color: #ffffff;"><strong>{}</strong></span></h4>""".format(nameMandarin)+"""
<p><span style="color: #ffffff;"><strong>{}</strong></span></p>""".format(nameEnglish)+"""
</td>
</tr>
<tr style="height: 18px;">
<td style="width: 100px; height: 18px;">
<p><strong>行經路線<p>
</td>
<td style="width: 200px; height: 18px;">{}</td>""".format(busstr)+"""
</tr>
</tbody>
</table>
<p>&nbsp;</p>
</html>
"""
    return html
#---

for i in j:
    longtitude = i['StationPosition']['PositionLon']
    latitude = i['StationPosition']['PositionLat']
    folium.Circle(
        location=[latitude, longtitude],
        radius=3,
        popup=folium.Popup(folium.Html(popup_html(i), script=True),parse_html=False, max_width=500),
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(m)

m.save('myMap.html')