import folium
from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
from folium.plugins import Search
import concurrent.futures
import polyline


m = folium.Map(location=[25.046436, 121.517463], zoom_start=11,tiles="Cartodb Positron", max_zoom=25)


#---
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
big_feature_group = folium.FeatureGroup(name="公車路線")
big_feature_group.add_to(m)
for i in route:
    if(i[1]!=''):
        feature_group = folium.FeatureGroup(name = i[0])
        feature_group.add_to(big_feature_group)
        folium.PolyLine(
            locations=polyline.decode(i[1]),
            popup="""<img src=\"""" + imagelist[i[0]] + """\">""",
            weight=3,
            color='red'
        ).add_to(feature_group)
        print(imagelist[i[0]])
    


folium.LayerControl(autoZIndex=False).add_to(m)
m.save('route.html')