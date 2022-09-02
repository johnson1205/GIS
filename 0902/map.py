from lib2to3.pytree import convert
from turtle import width
import bs4, requests, os, json, folium, tqdm
from folium.plugins import Search
import concurrent.futures
import folium
import polyline

#---routeimage
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
#---

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



m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=11, control_scale=True, max_zoom=25)

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
def popup_imgaehtml(i):
    img = ""
    img = imagelist[i[0]]
    routename = ""
    try:
        routename = i[0]
    except:
        routename=img
    html = """
    <!DOCTYPE html>
    <html>
    <tbody>
    <a href=\""""+img+"""\">{}</a>""".format(routename)+"""
    </tbody>
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
        popup=folium.Popup(folium.Html(popup_html(i), script=True),parse_html=False, max_width="100%"),
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(m)

#-------------------------------------station
#-------------------------------------route

routejsfileNewTaipei = open("routeNewTaipei.json", 'r', encoding='UTF-8')
routejswordNewTaipei = routejsfileNewTaipei.read()
j3= json.loads(routejswordNewTaipei)
routejsfileTaipei = open("routeTaipei.json", 'r', encoding='UTF-8')
routejswordTaipei = routejsfileTaipei.read()
j4= json.loads(routejswordTaipei)
j5=j3+j4

route=[]
for i in j5:
    rtpoly = ""
    try:
        rtpoly=i["EncodedPolyline"]
    except:
        rtpoly=""
    if(rtpoly==""):
        continue
    rtname = ""
    try:
        rtname=i["RouteName"]["Zh_tw"]
    except:
        rtname=""
    
    route.append([rtname, rtpoly])

route.sort(key=lambda x:x[0])
big_feature_group = folium.FeatureGroup(name="公車路線", show=False)
big_feature_group.add_to(m)
for i in route:
    if(i[1]!=''):
        feature_group = folium.FeatureGroup(name = i[0])
        feature_group.add_to(big_feature_group)
        folium.PolyLine(
            locations=polyline.decode(i[1]),
            popup=folium.Popup(folium.Html(popup_imgaehtml(i), script=True),parse_html=False, max_width=150),
            weight=3,
            color='red'
        ).add_to(feature_group)
    


folium.LayerControl(autoZIndex=False).add_to(m)

m.save('index.html')