# -*- coding: utf-8 -*-
# @Time    : 2026/10/10 16:40
# @Author  : Dragonkeep
# @Modified: 2026/01/19 15:30
# @Modified By: Brokenpoems
# @File    : MapAPITest.py

import requests
import json
import re
import dotenv
dotenv.load_dotenv()
BaiDu_AK = dotenv.get_key(".env", "BAIDU_AK")  # 在这里填写百度地图API密钥
Amap_AK = dotenv.get_key(".env", "AMAP_AK")  # 在这里填写高德地图API密钥
Amap_SK = dotenv.get_key(".env", "AMAP_SK")  # 在这里填写高德地图API密钥对应的secret
Tencent_AK = dotenv.get_key(".env", "TENCENT_AK")  # 在这里填写腾讯地图API密钥
Google_AK = dotenv.get_key(".env", "GOOGLE_AK")  # 在这里填写谷歌地图API密钥
TianTu_TK = dotenv.get_key(".env", "TianTu_TK")   # 在这里填写天地图API密钥
google_proxies = {
    "http": "socks5://127.0.0.1:11451",
    "https": "socks5://127.0.0.1:11451",
}  # 主要用于Google地图API请求，如不需要可设置为None
# 测试百度地图API AK是否可以使用


def BaiduMapAPI():
    result = {
        "Server_API": False,
        "Referer_Whitelist": False,
    }
    # 1. 服务端API有效性检测
    api_url = "http://api.map.baidu.com/geocoding/v3/"
    params = {"address": "北京天安门", "output": "json", "ak": BaiDu_AK}
    try:
        r_api = requests.get(api_url, params=params, timeout=5)
        data = r_api.json()
        # print(data)
        if data.get("status") == 0:
            result["Server_API"] = True
            result["Info"] = r_api.text
    except Exception as e:
        print(f"[!] 服务端API请求异常: {e}")

    # 2. Referer白名单检测（设置非白名单域名）
    headers = {"Referer": "http://example.com"}
    try:
        r_url = f"https://api.map.baidu.com/geocoding/v3/"
        r_ref = requests.get(r_url, params=params, headers=headers, timeout=5)
        # print(r_ref.text)
        if data.get("status") == 0:
            result["Referer_Whitelist"] = True
            results["Info"] = r_ref.text
    except Exception as e:
        print(f"[!] Referer检测异常: {e}")

    return result

# 测试高德API Key是否可以使用


def GaoDeMapAPI():
    results = {
        "Status": False
    }
    params = {"key": Amap_AK, "jscode": Amap_SK}
    print(params)
    # 测试webapi接口
    try:
        print("正在测试高德webapi...")
        api_url = "https://restapi.amap.com/v3/direction/walking?&origin=116.434307,39.90909&destination=116.434446,39.90816"
        r = requests.get(api_url, params=params, timeout=5)
        print("请求URL:", r.request.url)
        print("响应数据:", r.text)
        data = r.json()
        if data.get("status") == "1":
            results["Status"] = True
            results["Info"] = r.text
        else:
            results["Reason_webapi"] = data.get("info", r.text)
    except Exception as e:
        pass
     # 测试JS-API接口
    try:
        print("正在测试高德JS-API接口...")
        api_url = "https://restapi.amap.com/v3/geocode/regeo?s=rsv3&location=116.434446,39.90816&platform=JS"
        r = requests.get(api_url, params=params, timeout=5)
        print("请求URL:", r.request.url)
        print("响应数据:", r.text)
        data = r.json()
        if data.get("status") == "1":
            results["Status"] = True
            results["Info"] = r.text
        else:
            results["Reason_jsapi"] = data.get("info", r.text)
    except Exception as e:
        pass
    # 测试小程序接口
    try:
        print("正在测试高德小程序接口...")
        api_url = "https://restapi.amap.com/v3/geocode/regeo?&location=117.19674%2C39.14784&extensions=all&s=rsx&platform=WXJS&appname=c589cf63f592ac13bcab35f8cd18f495&sdkversion=1.2.0&logversion=2.0"
        r = requests.get(api_url, params=params, timeout=5)
        data = r.json()
        print("请求URL:", r.request.url)
        print("响应数据:", r.text)
        if data.get("status") == "1":
            results["Status"] = True
            results["Info"] = r.text
        else:
            results["Reason_wxapp"] = data.get("info", r.text)
    except Exception as e:
        pass
    return results

# 测试Google Maps API Key是否可以使用


def GoogleMapAPI():
    results = {
        "Status": False,
        "Reason": ""
    }

    params = {"key": Google_AK, "address": "Beijing"}
    try:
        api_url = "https://maps.googleapis.com/maps/api/geocode/json"
        r = requests.get(api_url, params=params, timeout=10, proxies=google_proxies)
        data = r.json()
        if data.get("status") == "OK":
            results["Status"] = True
            results["Info"] = r.text
        else:
            results["Info"] = r.text
    except Exception as e:
        print(f"[!] Google Maps API请求异常: {e}")
    return results

# 测试腾讯地图API Key是否可以使用


def TencentMapAPI():
    results = {
        "Status": False,
        "Reason": ""
    }
    params = {"key": Tencent_AK, "address": "北京"}
    try:
        api_url = "https://apis.map.qq.com/ws/geocoder/v1/"
        r = requests.get(api_url, params=params, timeout=5)
        data = r.json()
        if data.get("status") == 0:
            results["Status"] = True
            results["Info"] = r.text
        else:
            results["Reason"] = data.get("message", "未知错误")
    except Exception as e:
        print(f"[!] 腾讯地图API请求异常: {e}")
    return results


def TianTuMapAPI():
    results = {
        "SDK_Load": False,
        "Geocoder_API": False,
        "Vector_Tile": False,
        "Image_Tile": False,
        "Terrain_Tile": False,
        "Info": ""
    }

    Headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/85.0.4183.121 Safari/537.36"
    }

    # 1. 检测 SDK 是否能正常加载
    try:
        sdk_url = f"http://api.tianditu.gov.cn/api?v=4.0&tk={TianTu_TK}"
        r_sdk = requests.get(sdk_url, headers=Headers, timeout=5)
        if r_sdk.status_code == 200 and "天地图" in r_sdk.text:
            results["SDK_Load"] = True
        else:
            results["Info"] += f"SDK加载异常({r_sdk.status_code});"
    except Exception as e:
        results["Info"] += f"SDK加载异常: {e};"

    # 2. 测试地理编码（geocoder）接口
    try:
        api_url = "https://api.tianditu.gov.cn/geocoder"
        params = {
            "tk": TianTu_TK,
            "postStr": '{"lon":116.481488,"lat":39.990464,"ver":1}',
            "type": "0",
            "s": "rsv3"
        }
        r_api = requests.get(api_url, headers=Headers,
                             params=params, timeout=5)
        data = r_api.json()
        if data.get("status") == "0":
            results["Geocoder_API"] = True
        else:
            results["Info"] += f"Geocoder返回: {data.get('msg', data)};"
    except Exception as e:
        results["Info"] += f"地理编码接口异常: {e};"

    # 3. 检测矢量瓦片(vec_w)
    try:
        tile_url = f"https://t0.tianditu.gov.cn/DataServer?T=vec_w&x=1&y=1&l=1&tk={key}"
        r_tile = requests.get(tile_url, headers=Headers, timeout=5)
        if r_tile.status_code == 200 and r_tile.headers.get("Content-Type", "").startswith("image"):
            results["Vector_Tile"] = True
        else:
            results["Info"] += f"矢量瓦片返回: {r_tile.text[:60]};"
    except Exception as e:
        results["Info"] += f"矢量瓦片异常: {e};"

    # 4. 检测影像瓦片(img_w)
    try:
        tile_url = f"https://t0.tianditu.gov.cn/DataServer?T=img_w&x=1&y=1&l=1&tk={key}"
        r_img = requests.get(tile_url, headers=Headers, timeout=5)
        if r_img.status_code == 200 and r_img.headers.get("Content-Type", "").startswith("image"):
            results["Image_Tile"] = True
        else:
            results["Info"] += f"影像瓦片返回: {r_img.text[:60]};"
    except Exception as e:
        results["Info"] += f"影像瓦片异常: {e};"

    # 5. 检测地形瓦片(ter_w)
    try:
        tile_url = f"https://t0.tianditu.gov.cn/DataServer?T=ter_w&x=1&y=1&l=1&tk={key}"
        r_ter = requests.get(tile_url, headers=Headers, timeout=5)
        if r_ter.status_code == 200 and r_ter.headers.get("Content-Type", "").startswith("image"):
            results["Terrain_Tile"] = True
        else:
            results["Info"] += f"地形瓦片返回: {r_ter.text[:60]};"
    except Exception as e:
        results["Info"] += f"地形瓦片异常: {e};"

    return results


if __name__ == "__main__":
    if BaiDu_AK:
        results = BaiduMapAPI()
        print("百度地图API密钥检测结果:")
        for k, v in results.items():
            status = "可用" if v else "不可用"
            print(f"{k}: {status}")
        print()
    if Amap_AK:
        results = GaoDeMapAPI()
        print("高德地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
        print()
    if Google_AK:
        results = GoogleMapAPI()
        print("Google地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
        print()
    if Tencent_AK:
        results = TencentMapAPI()
        print("腾讯地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
        print()
    if TianTu_TK:
        results = TianTuMapAPI()
        print("天地图API密钥检测结果:")
        for k, v in results.items():
            print(f"{k}: {v}")
        print()
