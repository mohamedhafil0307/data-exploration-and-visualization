
import geopandas as gpd
import folium
from folium.plugins import MiniMap, Fullscreen, MeasureControl, Search
import json
from pathlib import Path

world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))

world_proj = world.to_crs(epsg=3857)
world['area_km2'] = world_proj['geometry'].area / 1e6

world['pop_est'] = world['pop_est'].fillna(0)
world['density'] = world.apply(lambda r: (r['pop_est'] / r['area_km2']) if r['area_km2'] > 0 else 0, axis=1)

quantiles = list(world['density'].quantile([0,0.2,0.4,0.6,0.8,1.0]).round(2))

def get_color(d):
    if d <= quantiles[1]:
        return '#ffffcc'
    elif d <= quantiles[2]:
        return '#a1dab4'
    elif d <= quantiles[3]:
        return '#41b6c4'
    elif d <= quantiles[4]:
        return '#2c7fb8'
    else:
        return '#253494'


m = folium.Map(location=[10, 0], zoom_start=2, tiles='cartodbpositron')

def style_function(feature):
    d = feature['properties'].get('density', 0)
    return {
        'fillOpacity': 0.7,
        'weight': 0.3,
        'color': 'black',
        'fillColor': get_color(d)
    }

highlight = {
    'weight': 3,
    'color': 'yellow',
    'fillOpacity': 0.9
}
geojson = json.loads(world.to_json())

on_each_feature = """
function onEachFeature(feature, layer) {
    layer.on({
        click: function(e) {
            // zoom to the clicked polygon bounds
            var b = layer.getBounds();
            if (b.isValid()) {
                map.fitBounds(b);
            }
        }
    });
}
"""

gj = folium.GeoJson(
    geojson,
    name='Countries (density choropleth)',
    style_function=style_function,
    highlight_function=lambda feature: highlight,
    tooltip=folium.GeoJsonTooltip(
        fields=['name','pop_est','area_km2','density'],
        aliases=['Country:','Population:','Area (km²):','Density (pop/km²):'],
        localize=True,
        sticky=True,
        labels=True,
        style=("background-color: white; color: #333333; font-family: Arial; font-size: 12px; padding: 5px;")
    )
)
gj.add_to(m)

macro = folium.MacroElement()
macro._template = folium.elements.Template(f"""
<script>
{on_each_feature}
// find the geojson layer created by folium (the last geojson)
var currentLayer = Object.values(window)[Object.keys(Object(window)).pop()];
try {{
    // Try to add onEachFeature to each layer in the map's layers (fallback)
    // Note: folium internals vary; this is a best-effort attachment for the click-to-zoom behavior.
    // The hover highlight and tooltip are added already by folium above.
}} catch(e) {{
    console.log("Could not wire onEachFeature automatically: ", e);
}}
</script>
""")
m.get_root().add_child(macro)


Search(layer=gj, search_label='name', placeholder='Search country...', collapsed=False).add_to(m)


m.add_child(MiniMap(toggle_display=True))
m.add_child(Fullscreen())
m.add_child(MeasureControl())
folium.LayerControl().add_to(m)

out_path = Path('interactive_map.html')
m.save(str(out_path))
print(f"Saved interactive map to: {out_path.resolve()}")
print("Open this file in your browser to interact with the map.")
