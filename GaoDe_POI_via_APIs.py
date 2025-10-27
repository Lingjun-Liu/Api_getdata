# 文件名: GaoDe_POI_via_API.py
# @desc: 利用高德API下载POI数据

import requests
import pandas as pd
import os
# import transCoordinateSystem as tcs

amp_api_key = '你的高德API密钥'
req_url_pref = "https://restapi.amap.com/v3/place/text?"

page_size = 25
page_num = 1

rep_params = {
    "types": "高等院校",
    "city": "西安",
    "offset": page_size,
    "page": page_num,
    "extensions": "base",
    "key": amp_api_key,
    "children": 1,
    "citylimit": "true"
}

def get_poi_from_amap():
    """从高德地图API下载POI数据"""
    result = pd.DataFrame()
    i = 1
    while True:
        print("📄 正在抓取第", i, "页数据...")
        rep_params["page"] = i
        response = requests.get(req_url_pref, params=rep_params)
        data = response.json()
        count = int(data["count"])
        if count == 0:
            break

        for poi in data["pois"]:
            name = poi["name"]
            address = poi["address"]
            location = poi["location"]
            lon, lat = map(float, location.split(","))

            busi_data = [{
                "name": name,
                "address": address,
                "lon": lon,
                "lat": lat
            }]
            result = pd.concat([result, pd.DataFrame(busi_data)], ignore_index=True)

        i += 1

    # 一次性写出
    output_path = os.path.join(os.getcwd(), "poi_school.xlsx")
    result.to_excel(output_path, index=False)
    print("✅ 已保存至:", output_path)


if __name__ == '__main__':
    get_poi_from_amap()
