import requests
import urllib.parse

key = "d42e7822-787d-4cb9-bd37-29da72844808"  # ***Key API*** 
geocode_url = "https://graphhopper.com/api/1/geocode?"
route_url = "https://graphhopper.com/api/1/route?"

def geocoding(location, key):  # ***Geocodificación***
    while location.strip() == "":
        location = input("Ingrese la ubicación nuevamente: ")

    url = geocode_url + urllib.parse.urlencode({"q": location, "limit": "1", "key": key})
    replydata = requests.get(url)
    json_status = replydata.status_code
    json_data = replydata.json()

    if json_status == 200 and len(json_data["hits"]) != 0:
        hit = json_data["hits"][0]
        lat = hit["point"]["lat"]
        lng = hit["point"]["lng"]
        name = hit["name"]
        value = hit.get("osm_value", "desconocido")
        country = hit.get("country", "")
        state = hit.get("state", "")

        if state and country:
            new_loc = f"{name}, {state}, {country}"
        elif country:
            new_loc = f"{name}, {country}"
        else:
            new_loc = name

        print("URL de la API de Geocodificación para " + new_loc + " (Tipo de ubicación: " + value + ")")
        print(url)
    else:
        lat = "null"
        lng = "null"
        new_loc = location
        if json_status != 200:
            print("Estado de la API de Geocodificación: " + str(json_status))
            print("Mensaje de error: " + json_data.get("message", "No se proporcionó mensaje"))

    return json_status, lat, lng, new_loc

# *** Bucle principal ***
while True:
    print("\n+++++++++++++++++++++++++++++++++++++++++++++")
    print("Vehículos disponibles en Graphhopper:")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    print("car (auto), bike (bicicleta), foot (a pie)")
    print("+++++++++++++++++++++++++++++++++++++++++++++")
    profile = ["car", "bike", "foot"]
    vehicle = input("Ingrese un tipo de vehículo de la lista anterior: ")
    if vehicle.lower() in ["s", "quit"]:
        break
    elif vehicle not in profile:
        print("No se ingresó un tipo de vehículo válido. Se usará 'auto' por defecto.")
        vehicle = "car"

    loc1 = input("Ubicación de inicio: ")
    if loc1.lower() in ["s", "quit"]:
        break
    orig = geocoding(loc1, key)

    loc2 = input("Ubicación de destino: ")
    if loc2.lower() in ["s", "quit"]:
        break
    dest = geocoding(loc2, key)

    print("=================================================")

    if orig[0] == 200 and dest[0] == 200:
        op = "&point=" + str(orig[1]) + "%2C" + str(orig[2])
        dp = "&point=" + str(dest[1]) + "%2C" + str(dest[2])
        paths_url = route_url + urllib.parse.urlencode({"key": key, "vehicle": vehicle}) + op + dp

        response = requests.get(paths_url)
        paths_status = response.status_code
        paths_data = response.json()

        print("Estado de la API de Ruteo: " + str(paths_status))
        print("URL utilizada en la API de Ruteo:")
        print(paths_url)
        print("=================================================")
        print("Dirección desde " + orig[3] + " hasta " + dest[3] + " usando " + vehicle)
        print("=================================================")

        if paths_status == 200:
            distance = paths_data["paths"][0]["distance"]
            time_ms = paths_data["paths"][0]["time"]

            km = distance / 1000
            miles = km / 1.61
            sec = int(time_ms / 1000 % 60)
            min = int(time_ms / 1000 / 60 % 60)
            hr = int(time_ms / 1000 / 60 / 60)

            fuel_consumption_rates = {
                "car": 8,
                "bike": 3,
                "foot": 0
            }
            consumption_rate = fuel_consumption_rates.get(vehicle, 0)
            fuel_used = (km * consumption_rate) / 100

            print("Distancia del viaje: {:.1f} km / {:.1f} millas".format(km, miles))
            print("Duración del viaje: {:02d}:{:02d}:{:02d} (hh:mm:ss)".format(hr, min, sec))
            print("Combustible estimado: {:.1f} litros".format(fuel_used))
            print("=================================================")
            print("Instrucciones paso a paso:")
            print("=================================================")

            for each in range(len(paths_data["paths"][0]["instructions"])):
                path = paths_data["paths"][0]["instructions"][each]["text"]
                dist = paths_data["paths"][0]["instructions"][each]["distance"]
                print("{0} ( {1:.1f} km / {2:.1f} millas )".format(path, dist / 1000, dist / 1000 / 1.61))
            print("=================================================")
        else:
            print("Error, mensaje: " + paths_data.get("mensaje", "No hay rutas disponibles"))
            print("*************************************************")
    else:
        print("No se pudieron obtener coordenadas válidas para ambas ubicaciones.")
