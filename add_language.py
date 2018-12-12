import openpyxl
import os
import json

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
    path_language_table = os.path.join("M:\BEQUIET\workspace\data", "country_languange_dict.xlsx")
    # 获得国家-语言表
    d = get_country2language_table(path_language_table)

    path_poc_json = os.path.join("affi_info.json")
    js_poc = json.load(open(path_poc_json))
    for k, v in js_poc.items():
        country = v.setdefault('country', '')
        if country is not '':
            js_poc[k]['language'] = d.setdefault(country, "")
    json.dump(js_poc, open("affi_info_language.json", "w"))
