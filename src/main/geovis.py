import folium
import geopandas as gpd

# Load California school districts shapefile
districts_shapefile = "California_School_District_Areas_2020-21.shp"
california_districts = gpd.read_file(districts_shapefile)

# Load underfunded school districts data
underfunded_districts = {}  # Your underfunded districts data (district name: funding gap)

# Merge data
california_districts['funding_gap'] = california_districts['district_name'].map(underfunded_districts)

# Create a map centered around California
m = folium.Map(location=[36.7783, -119.4179], zoom_start=6)

# Add school district boundaries with color-coded funding gap
folium.Choropleth(
    geo_data=california_districts,
    name='choropleth',
    data=california_districts,
    columns=['district_name', 'funding_gap'],
    key_on='feature.properties.district_name',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='Funding Gap'
).add_to(m)

# Display the map
m.save('map.html')
