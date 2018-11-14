import json
import requests
import proxy_provider
import os

__GOOGLE_KEY = "AIzaSyDDzBNqMLO96aIRbNh18LqnVeagfJK1-s8"
__HOST_lo_la = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=" + __GOOGLE_KEY
__HOST_loc = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=" + __GOOGLE_KEY

__MAX_TRY = 6


def toCountry(keys):
    if type(keys) in {list, tuple}:
        url = __HOST_lo_la.format(keys[0], keys[1])
    else:
        url = __HOST_loc.format(keys.replace(" ", "+"))
    resp = requests.get(url, proxies=proxy_provider.get_proxy(), verify=False)

    if resp.status_code == 200:
        return resp.text
    if resp.status_code == 503:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


if __name__ == '__main__':
    dir_result = os.path.join("loc")
    with open("all_affi.json", "r") as f:
        js = json.load(f)
        for k, v in js.items():
            file_res = os.path.join(dir_result, k)
            if v['lo'] == v['la'] == 0:
                keys = v['name']
            else:
                keys = (v['la'], v['lo'])

            have_try = 0
            while have_try < __MAX_TRY:
                try:
                    have_try += 1
                    loc_info = toCountry(keys)
                    with open(file_res, "w", encoding="utf-8") as fw:
                        fw.write(loc_info)
                    break
                except Exception as e:
                    print(k, str(e))

