from lib2to3.pytree import convert
import bs4, requests, os, json, folium, tqdm
import concurrent.futures



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

m = folium.Map([25.046436, 121.517463], tiles="Cartodb Positron", zoom_start=11, control_scale=True)
outfile = open("stationlist.txt", "w", encoding='UTF-8')

#---
def popup_html(i):
    nameMandarin = i['StopName']['Zh_tw']
    nameEnglish = ""
    try:
        nameEnglish=i['StopName']['En']
    except:
        nameEnglish=""
    html = """
<!DOCTYPE html>
<html>
<table style="border-collapse: collapse; width: 300px; height: 36px;" border="1">
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
<td style="width: 200px; height: 18px;">&nbsp;</td>
</tr>
</tbody>
</table>
<p>&nbsp;</p>
</html>
"""
    return html
#---

for i in j:
    longtitude = i['StopPosition']['PositionLon']
    latitude = i['StopPosition']['PositionLat']
    stopname = i['StopName']['Zh_tw']
    outfile.write(stopname+' '+str(latitude)+str(longtitude)+'\n')
    folium.Circle(
        location=[latitude, longtitude],
        radius=3,
        popup=folium.Popup(folium.Html(popup_html(i), script=True),parse_html=False, max_width=300),
        color='#3186cc',
        fill=True,
        fill_color='#3186cc'
    ).add_to(m)

m.save('myMap.html')