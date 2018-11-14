import os
import json

path_all = os.path.join("all.json")
path_aff = os.path.join("affiliation_lo_la_11-8.json")

path_res = os.path.join("all_affi.json")

js_all = json.load(open(path_all))
js_aff = json.load(open(path_aff))
print(len(js_aff), len(js_all))
for k, v in js_all.items():
    if k not in js_aff.keys():
        info = {'name': v, 'lo': 0.0, 'la': 0.0}
        js_aff[k] = info


print(len(js_aff), len(js_all))
json.dump(js_aff, open(path_res, "w"))
