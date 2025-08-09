

import os
import json
import tempfile
from pathlib import Path

import geopandas as gpd
import pandas as pd
import folium
from folium.features import GeoJson, GeoJsonTooltip
import branca.colormap as cm

DATA_DIR = Path("data")
OUTPUT_DIR = Path("output")
OUTPUT_DIR.mkdir(exist_ok=True)

WORLD_ATTR_CSV = DATA_DIR / "world_data.csv"               
INDIA_STATES_GEOJSON = DATA_DIR / "india_states.geojson" 
INDIA_DISTRICTS_GEOJSON = DATA_DIR / "india_districts.geojson"  
INDIA_STATES_ATTR_CSV = DATA_DIR / "india_states_data.csv"      
INDIA_DISTRICTS_ATTR_CSV = DATA_DIR / "india_districts_data.csv"


WORLD_GEO_KEY = "name"        
WORLD_ATTR_KEY = "name"
INDIA_STATES_GEO_KEY = "st_nm"  
INDIA_DISTRICTS_GEO_KEY = "DISTRICT" 
INDIA_DISTRICTS_ATTR_KEY = "district_name"



def ensure_dir(path: Path):
    path.mkdir(parents=True, exist_ok=True)


def load_or_make_example_world_data(world_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """If an attribute CSV for the world is present, load it and return. Otherwise create
    a small example dataframe keyed by country name with a numeric 'value' column."""
    if WORLD_ATTR_CSV.exists():
        df = pd.read_csv(WORLD_ATTR_CSV)
        return df
    
    df = (
        world_gdf[[WORLD_GEO_KEY]]
        .copy()
        .rename(columns={WORLD_GEO_KEY: WORLD_ATTR_KEY})
    )
  
    df["value"] = (pd.np.random.rand(len(df)) * 100).round(1)
    return df


def load_or_make_example_india_states_data(states_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    if INDIA_STATES_ATTR_CSV.exists():
        return pd.read_csv(INDIA_STATES_ATTR_CSV)
    df = (
        states_gdf[[INDIA_STATES_GEO_KEY]]
        .copy()
        .rename(columns={INDIA_STATES_GEO_KEY: INDIA_STATES_ATTR_KEY})
    )
    df["value"] = (pd.np.random.rand(len(df)) * 100).round(1)
    return df


def load_or_make_example_india_districts_data(districts_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    if INDIA_DISTRICTS_ATTR_CSV.exists():
        return pd.read_csv(INDIA_DISTRICTS_ATTR_CSV)
    key = INDIA_DISTRICTS_GEO_KEY
    if key not in districts_gdf.columns:
        key = districts_gdf.columns[0]
    df = districts_gdf[[key]].copy().rename(columns={key: INDIA_DISTRICTS_ATTR_KEY})
    df["value"] = (pd.np.random.rand(len(df)) * 100).round(1)
    return df


def create_world_map():
    print("Loading world base geometry from GeoPandas' naturalearth_lowres dataset...")
    world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))

    world_attr = load_or_make_example_world_data(world)

  
    left = world.rename(columns={WORLD_GEO_KEY: WORLD_ATTR_KEY})
    merged = left.merge(world_attr, on=WORLD_ATTR_KEY, how="left")

 
    centroid = merged.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=2, tiles="cartodbpositron")

    values = merged["value"].fillna(0)
    colormap = cm.LinearColormap(["#f7fbff", "#08306b"], vmin=values.min(), vmax=values.max())
    colormap.caption = "Value"
    colormap.add_to(m)

    def style_function(feat):
        v = feat["properties"].get("value")
        if v is None:
            return {"fillOpacity": 0.1, "weight": 0.4}
        return {"fillColor": colormap(v), "fillOpacity": 0.7, "weight": 0.3}

    gj = GeoJson(
        merged.to_json(),
        name="World choropleth",
        style_function=style_function,
        tooltip=GeoJsonTooltip(fields=[WORLD_ATTR_KEY, "value"], aliases=["Country", "Value"], localize=True),
    )
    gj.add_to(m)
    folium.LayerControl().add_to(m)

    out = OUTPUT_DIR / "world_map.html"
    m.save(str(out))
    print(f"Saved world map to {out}")


def create_india_states_map():
    if not INDIA_STATES_GEOJSON.exists():
        print(f"India states GeoJSON not found at {INDIA_STATES_GEOJSON}. Please provide it and re-run.")
        return

    states = gpd.read_file(str(INDIA_STATES_GEOJSON))
    # try find best key column
    if INDIA_STATES_GEO_KEY not in states.columns:
        # fallback: try common column names
        for candidate in ["st_nm", "STATE_NAME", "STATE", "NAME", "name"]:
            if candidate in states.columns:
                states[INDIA_STATES_GEO_KEY] = states[candidate]
                break

    states_attr = load_or_make_example_india_states_data(states)
    merged = states.merge(states_attr, left_on=INDIA_STATES_GEO_KEY, right_on=INDIA_STATES_ATTR_KEY, how="left")

    centroid = merged.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=5, tiles="cartodbpositron")

    values = merged["value"].fillna(0)
    colormap = cm.LinearColormap(["#ffffcc", "#800026"], vmin=values.min(), vmax=values.max())
    colormap.caption = "Value (states)"
    colormap.add_to(m)

    def style_function(feat):
        v = feat["properties"].get("value")
        if v is None:
            return {"fillOpacity": 0.05, "weight": 0.4}
        return {"fillColor": colormap(v), "fillOpacity": 0.7, "weight": 0.4}

    gj = GeoJson(
        merged.to_json(),
        name="India States",
        style_function=style_function,
        tooltip=GeoJsonTooltip(fields=[INDIA_STATES_GEO_KEY, "value"], aliases=["State", "Value"], localize=True),
    )
    gj.add_to(m)
    folium.LayerControl().add_to(m)

    out = OUTPUT_DIR / "india_states_map.html"
    m.save(str(out))
    print(f"Saved India states map to {out}")


def create_india_districts_map():
    if not INDIA_DISTRICTS_GEOJSON.exists():
        print(f"India districts GeoJSON not found at {INDIA_DISTRICTS_GEOJSON}. Please provide it and re-run.")
        return

    districts = gpd.read_file(str(INDIA_DISTRICTS_GEOJSON))
    key = INDIA_DISTRICTS_GEO_KEY if INDIA_DISTRICTS_GEO_KEY in districts.columns else districts.columns[0]
    districts_attr = load_or_make_example_india_districts_data(districts)

    merged = districts.merge(districts_attr, left_on=key, right_on=INDIA_DISTRICTS_ATTR_KEY, how="left")

    centroid = merged.geometry.unary_union.centroid
    m = folium.Map(location=[centroid.y, centroid.x], zoom_start=6, tiles="cartodbpositron")

    values = merged["value"].fillna(0)
    colormap = cm.LinearColormap(["#fff5f0", "#67000d"], vmin=values.min(), vmax=values.max())
    colormap.caption = "Value (districts)"
    colormap.add_to(m)

    def style_function(feat):
        v = feat["properties"].get("value")
        if v is None:
            return {"fillOpacity": 0.03, "weight": 0.2}
        return {"fillColor": colormap(v), "fillOpacity": 0.6, "weight": 0.2}

  
    tooltip_fields = [key, "value"]
    aliases = ["District", "Value"]

    gj = GeoJson(
        merged.to_json(),
        name="India Districts",
        style_function=style_function,
        tooltip=GeoJsonTooltip(fields=tooltip_fields, aliases=aliases, localize=True),
    )
    gj.add_to(m)
    folium.LayerControl().add_to(m)

    out = OUTPUT_DIR / "india_districts_map.html"
    m.save(str(out))
    print(f"Saved India districts map to {out}")



if __name__ == "__main__":
    print("Starting cartographic visualization builder...")
    create_world_map()
    create_india_states_map()
    create_india_districts_map()
    print("All done. Check the output/ folder for HTML files.")
