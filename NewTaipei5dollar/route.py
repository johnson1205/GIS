#https://ebus.gov.taipei/ProjectBus/DestinyBus

import folium
from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
from folium.plugins import Search
import concurrent.futures
import polyline


m = folium.Map(location=[25.046436, 121.517463], zoom_start=11,tiles="Cartodb Positron", max_zoom=25)

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


buslist = ["249","575","581","587","666華梵大學","666烏塗窟","666皇帝殿","677正","677副","704","716","778","781","788","788海科館","788區","791","791繞貢寮","791經貢寮區衛生","795往平溪","795往木柵","795往十分寮","801","807","808","815","849","849屈尺社區","856","862","863","947","953","953區","965","966","981","紅26","藍41","藍41延和","綠12","橘20"]

route.sort(key=lambda x:x[0])
big_feature_group = folium.FeatureGroup(name="公車路線")
big_feature_group.add_to(m)
for i in route:
    if(i[0] in buslist):
        if(i[1]!=''):
            feature_group = folium.FeatureGroup(name = i[0])
            feature_group.add_to(big_feature_group)
            folium.PolyLine(
                locations=polyline.decode(i[1]),
                popup=i[0],
                weight=3,
                color='red'
            ).add_to(feature_group)
    


folium.LayerControl(autoZIndex=False).add_to(m)
m.save('route.html')