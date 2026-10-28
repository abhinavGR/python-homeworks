import folium

mymap = folium.Map(location=[32.7767, -96.7970], zoom_start=14)

folium.TileLayer(
    tiles='https://{s}://{z}/{x}/{y}{r}.png',
    name='Cyber Grid',
    attr='CARTO'
).add_to(mymap)

mymap.save('dallas_cyber_grid.html')
print('New futuristic map created successfully!')
