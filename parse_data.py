import os
import json
import openpyxl


def set2file(s, fn):
    with open(fn, 'w', encoding="utf-8") as f:
        f.write("\n".join(s))


# 获得国家-语言对照表
def get_country2language_table(path_table):
    wb = openpyxl.load_workbook(path_table)
    sheet = wb.active

    dict_c2l = dict()
    for i in range(2, sheet.max_row + 1):
        country = sheet['A%s' % i].value.replace("\xa0", '').strip(" ")
        language = sheet['B%s' % i].value
        dict_c2l[country] = language

    return dict_c2l


if __name__ == '__main__':
    path_dir_raw_data = os.path.join("M:\BEQUIET\workspace\data\loc")

    path_poc_json = os.path.join("all_affi.json")

    js_poc = json.load(open(path_poc_json))
    # 剩余没有得到的id
    set_remains = set()

    path_language_table = os.path.join("M:\BEQUIET\workspace\data", "country_languange_dict.xlsx")
    dict_c2l = get_country2language_table(path_language_table)
    for k, v in js_poc.items():
        # 得到文件名
        path_raw_data = os.path.join(path_dir_raw_data, k)
        if os.path.isfile(path_raw_data):
            js_raw_data = json.load(open(path_raw_data, encoding="utf-8"))
            raw_results = js_raw_data.setdefault('results', dict())

            # 取第一个地理位置
            if len(raw_results) > 0:
                location = raw_results[0]
                address_components = location.setdefault('address_components', [])
                for c in address_components:
                    # 获得国家名称, 记录下来
                    if "country" in c['types']:
                        country = c['long_name']
                        js_poc[k]['country'] = country
                        js_poc[k]['language'] = dict_c2l.setdefault(country, "")
                        break
                    else:
                        # 否则， 国家置为空
                        js_poc[k]['country'] = ""
                        js_poc[k]['language'] = ''

                # 如果原来的经纬度数据缺失,则补全
                if v['la'] == v['lo'] == 0:
                    geometry = location.setdefault('geometry', [])
                    if geometry is not []:
                        lat = geometry['location']['lat']
                        lng = geometry['location']['lng']
                        js_poc[k]['la'] = lat
                        js_poc[k]['lo'] = lng
                        print(lat, lng)
        else:
            set_remains.add(k)

    set2file(set_remains, os.path.join("remains"))
    json.dump(js_poc, open("affi_info.json", "w"))


