import json
import requests
import proxy_provider
import os
import warnings
warnings.filterwarnings("ignore")

__GOOGLE_KEY = "AIzaSyDDzBNqMLO96aIRbNh18LqnVeagfJK1-s8"
__HOST_lo_la = "https://maps.googleapis.com/maps/api/geocode/json?latlng={},{}&key=" + __GOOGLE_KEY
__HOST_loc = "https://maps.googleapis.com/maps/api/geocode/json?address={}&key=" + __GOOGLE_KEY
__MAX_TRY = 6


def toCountry(keys):
    # construct the url
    if type(keys) in {list, tuple}:
        url = __HOST_lo_la.format(keys[0], keys[1]) # la lo
    else:
        url = __HOST_loc.format(keys.replace(" ", "+")) # place name
    resp = requests.get(url, proxies=proxy_provider.get_proxy(), verify=False)

    if resp.status_code == 200:
        return resp.text
    if resp.status_code == 503:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))
    else:
        raise Exception('Error: {0} {1}'.format(resp.status_code, resp.reason))


def get_remain(affi_info_path, path_remain, dir_result):
    # 将remain列表读出来
    id_remain = set()
    with open(path_remain, 'r', encoding='utf-8') as f:
        for line in f.readlines():
            line = line.strip()
            if len(line.strip()) < 0:
                continue
            id_remain.add(line)

    with open(affi_info_path, "r") as f:
        js = json.load(f)
        for k in id_remain:
            file_res = os.path.join(dir_result, k)
            v = js[k]
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
                    print("-------------%s-------------") % k
                    break
                except Exception as e:
                    print(k, str(e))


# 根据json文件，得到结果
def get_info(affi_info_path, dir_result):
    with open(affi_info_path, "r") as f:
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
                    print("-------------%s-------------" % k)
                    break
                except Exception as e:
                    print(k, str(e))


if __name__ == '__main__':
    dir_result = os.path.join("loc")
    path_remain = os.path.join("remains")
    path_raw_affi_info = os.path.join("affiliation_lo_la_12_11.json")
    get_info(path_raw_affi_info, dir_result)
