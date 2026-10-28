import folium
mymap = folium.Map(location=[32.7767, -96.7970], zoom_start=14)
folium.TileLayer('https://{s}://{z}/{x}/{y}{r}.png', name='Dark Grid', attr='CARTO').add_to(mymap)
mymap.save('dallas_complete_map.html')
print('Map created successfully!')
