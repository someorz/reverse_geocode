# -*- coding: utf-8 -*-
"""
Copyright © ZhouJun
Time: 2019/06/28 14:57
author: ZhouJun
mail: zhoujunseu@163.com

"""
token = ''
key = ''
ak = ''

import requests

def amap_geocode(name, key):
        base_url  = 'https://restapi.amap.com/v3/geocode/geo?address='
        url = base_url + name + '&output=JSON&key=' + key
        try:
                data=requests.get(url).json()
                location = data.get('geocodes')[0].get('location').split(',')
                lon = float(location[0])
                lat = float(location[1])
                return lon,lat
        except:
                return 0,0

def amap_regeo(lon, lat, key):
        base_url = 'https://restapi.amap.com/v3/geocode/regeo?output=json&location='
        url = base_url + str(lon) + ',' + str(lat) + '&key=' + key
        try:
                data=requests.get(url).json()
                addr = data.get('regeocode').get('formatted_address')
                return addr
        except:
                return 0

def tianditu_geocode(name, token):
        base_url = 'http://api.tianditu.gov.cn/geocoder?ds={"keyWord":"'
        url = base_url + name + '"}&tk=' + token
        try:
                data=requests.get(url).json()
                lon = float(data.get('location').get('lon'))
                lat = float(data.get('location').get('lat'))
                return lon,lat
        except:
                return 0,0

def tianditu_regeo(lon, lat, token):
        base_url = "http://api.tianditu.gov.cn/geocoder?postStr={'lon':"
        url = base_url+str(lon)+",'lat':"+str(lat)+",'ver':1}&type=geocode&tk="+token
        try:
                data=requests.get(url).json()
                addr = data.get('result').get('formatted_address')
                return addr
        except:
                return 0

def baidumap_geocode(name, ak):
        base_url = 'http://api.map.baidu.com/geocoding/v3/?address='
        url = base_url + name + '&output=json&ak=' + ak
        try:
                data=requests.get(url).json()
                lon = float(data.get('result').get('location').get('lng'))
                lat = float(data.get('result').get('location').get('lat'))
                return lon,lat
        except:
                return 0,0

def baidumap_regeo(lon, lat, ak):
        base_url = 'http://api.map.baidu.com/reverse_geocoding/v3/?ak='
        url = base_url+ak+'&output=json&coordtype=wgs84ll&location='+str(lat)+','+str(lon)
        try:
                data=requests.get(url).json()
                addr = data.get('result').get('formatted_address')
                return addr
        except:
                return 0

def geocode(name):
        #优先使用百度，数据多且准， 其次天地图，最后高德
        lon,lat = baidumap_geocode(name, ak)
        if lon==0:
                lon,lat = tianditu_geocode(name, token)
                if lon==0:
                        lon,lat = amap_geocode(name, key)
        return lon,lat

def regeo(lon,lat):
        #优先使用天地图， 其次高德，最后百度
        addr = tianditu_regeo(lon,lat,token)
        if addr == 0:
                addr = amap_regeo(lon,lat,key)
                if addr == 0:
                        addr = baidumap_regeo(lon,lat,ak)
        return addr
        
