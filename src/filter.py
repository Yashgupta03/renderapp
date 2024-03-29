import json

with open('refined.geojson') as response:
    geodata = json.load(response)

prec=10**4
for i in range(len(geodata["features"])):
    a=str(geodata["features"][i]["properties"]['District'])
    b=str(geodata["features"][i]["properties"]['STATE'])
    geodata["features"][i]["properties"]={'District':a.upper(),'STATE':b.upper()}
    t=geodata["features"][i]["geometry"]['type']
    if t=="Polygon":
        for j in range(len(geodata["features"][i]["geometry"]['coordinates'][0])):
            geodata["features"][i]["geometry"]['coordinates'][0][j][0]=float((int(geodata["features"][i]["geometry"]['coordinates'][0][j][0]*(prec)))/(prec))
            geodata["features"][i]["geometry"]['coordinates'][0][j][1]=float((int(geodata["features"][i]["geometry"]['coordinates'][0][j][1]*(prec)))/(prec))
    elif t=="MultiPolygon":
        for j in range(len(geodata["features"][i]["geometry"]['coordinates'])):
            for k in range(len(geodata["features"][i]["geometry"]['coordinates'][j][0])):
                geodata["features"][i]["geometry"]['coordinates'][j][0][k][0]=float((int(geodata["features"][i]["geometry"]['coordinates'][j][0][k][0]*(prec)))/(prec))
                geodata["features"][i]["geometry"]['coordinates'][j][0][k][1]=float((int(geodata["features"][i]["geometry"]['coordinates'][j][0][k][1]*(prec)))/(prec))


with open('./assets/update.geojson', 'w') as fp:
    json.dump(geodata, fp)