# -*- coding: utf-8 -*-
"""
Copyright © ZhouJun
Time: 2019/06/28 16:19
author: ZhouJun
mail: zhoujunseu@163.com

"""

import pandas as pd
from geocode import geocode, regeo

file = r'C:\Users\zhouj\Desktop\new.xlsx'
# 1 for geocode and 2 for regeocode
operator = 1
Name = '名称' ##地址名称所在的列的名字
Lon = 'lon' ##经度所在列的名字
Lat = 'lat' ##维度所在列的名字

def excel_geocode(file):
        new_file = file.split('.')[0]+'_new.xlsx'
        with pd.ExcelWriter(new_file) as writer: 
                df = pd.read_excel(file, sheet_name=None)
                for key in df.keys():
                        df0 = df[key]
                        names = df0[Name]
                        lon_ = []
                        lat_ = []
                        for name in names:
                               lon,lat = geocode(name)
                               lon_.append(lon)
                               lat_.append(lat)
                        lon = pd.Series(lon_)
                        lat = pd.Series(lat_)
                        df0.insert(df0.shape[1], 'lon', lon)
                        df0.insert(df0.shape[1], 'lat', lat)
                        df0.to_excel(writer, sheet_name=key, index=False)
                        print(key+' is done...')


def excel_regeocode(file):
        new_file = file.split('.')[0]+'_new.xlsx'
        with pd.ExcelWriter(new_file) as writer:
                df = pd.read_excel(file, sheet_name=None)
                for key in df.keys():
                        df0 = df[key]
                        lon = df0[Lon]
                        lat = df0[Lat]
                        loc = list(zip(lon,lat))
                        addr_ = []
                        for lon,lat in loc:
                                addr = regeo(lon,lat)
                                addr_.append(addr)
                        addr = pd.Series(addr_)
                        df0.insert(df0.shape[1], 'addr', addr)
                        df0.to_excel(writer, sheet_name=key, index=False)
                        print(key+' is done...')

if operator==1:
        excel_geocode(file)
else:
        excel_regeocode(file)