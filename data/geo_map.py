import requests


def get_map(river):
    str_coords = get_coords(river)
    coords = list(map(float, str_coords.split()))
    return get_link(coords, point=True)


def get_link(coords, type_map='map', point=False):
    toponym_longitude, toponym_latitude = coords
    delta = [0.04, 0.04]
    delta1, delta2 = delta
    map_params = {
        "ll": f'{toponym_longitude},{toponym_latitude}',
        "spn": f'{delta1},{delta2}',
        "l": f'{type_map}'
    }
    if point:
        map_params["pt"] = f'{toponym_longitude},{toponym_latitude},pm2vvl'
    map_api_server = "http://static-maps.yandex.ru/1.x/"
    params_string = '&'.join(f'{key}={value}' for (key, value) in map_params.items())
    return map_api_server + '?' + params_string


def get_coords(place):
    geocoder_api_server = "http://geocode-maps.yandex.ru/1.x/"
    geocoder_params = {
        "apikey": "40d1649f-0493-4b70-98ba-98533de7710b",
        "geocode": 'river ' + place,
        "format": "json"}

    response = requests.get(geocoder_api_server, params=geocoder_params)
    if not response:
        pass

    json_response = response.json()
    toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
    toponym_coodrinates = toponym["Point"]["pos"]
    return toponym_coodrinates


#  if __name__ == '__main__':
#      print(get_map('Shuy'))