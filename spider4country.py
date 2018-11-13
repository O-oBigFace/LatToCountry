import json
import requests
import proxy_provider
import os

__HOST = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=AIzaSyDDzBNqMLO96aIRbNh18LqnVeagfJK1-s8"


def toCountry(lat, lo):
    url = __HOST.format(lat, lo)
    resp = requests.get(url, proxies=proxy_provider.get_proxy(), verify=False)

    if resp.status_code == 200:
        return resp.text
    if resp.status_code == 503:
        # Inelegant way of dealing with the G captcha
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


if __name__ == '__main__':
    dir_result = os.path.join("loc")
    with open("affiliation_lo_la_11-8.json", "r") as f:
        js = json.load(f)
        for k, v in js.items():
            file_res = os.path.join(dir_result, k)
            if v['lo'] == v['la'] == 0:
                continue
            with open(file_res, "w", encoding="utf-8") as fw:
                loc_info = toCountry(v['la'], v['lo'])
                fw.write(loc_info)
            print(k)
