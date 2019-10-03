import folium
import pandas
from folium.plugins import MarkerCluster
data = pandas.read_csv("Volcanoes.txt")

lat=list(data["LAT"])
lon=list(data["LON"])
elev = list(data["ELEV"])
name = list(data["NAME"])
html = """
Volcano name:<br>
<a href="https://www.google.com/search?q=%%22%s%%22" target="_blank">%s</a><br>
Height: %s m
"""
def color_analyzer(elevation):
    if elevation <1000:
        return 'green'
    elif elevation <3000:
        return 'orange'
    else: return 'red'

map = folium.Map(location=[38.58,-99.89],zoom_start = 5, tiles= "CartoDB dark_matter")

fgv= folium.FeatureGroup("Volcanoes")
fgp = folium.FeatureGroup("Popular")
marker_cluster=MarkerCluster().add_to(map)
for lt, ln, el, name in zip(lat, lon, elev, name):
    iframe = folium.IFrame(html=html % (name, name, el), width=200, height=100)
    fgv.add_child(folium.CircleMarker(location=[lt, ln], radius=9, popup=folium.Popup(iframe), fill_color=color_analyzer(el),
                        color="gray", fill_opacity=0.9))

fgp.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(), style_function=
lambda x:{'fillColor':'white' if x['properties']['POP2005'] < 10000000
else'green' if x['properties']['POP2005'] < 100000000
else'yellow' if x['properties']['POP2005'] < 500000000
else 'orange' if x['properties']['POP2005'] < 1000000000 else 'red'}))

map.add_child(fgv)
map.add_child(fgp)
map.add_child(folium.LayerControl())
map.save("Map1.html")
